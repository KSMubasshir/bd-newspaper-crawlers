import time
import os
import re
import pickle
import json
import copy
import shutil
import constants
import traceback
from random import uniform
from tqdm import tqdm
from bs4 import BeautifulSoup
import constants
from queue import Queue, Empty
import multiprocessing
from multiprocessing.dummy import Pool, Lock
from sessions import TouchVPNSession


class SetQueue(Queue):
    def _init(self, maxsize=0):
        self.queue = set()

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


class CrawlerBase(object):
    def __init__(self, base_url, seed_links=[], out_dir='./', default_id='non-article-page',
                 max_concurrent_requests=constants.MAX_CONCURRENT_REQUESTS,
                 session_class=TouchVPNSession, *session_args, **session_kwargs):
        self.base_url = base_url
        self.sessions = [session_class(*session_args, **session_kwargs) for _ in range(max_concurrent_requests)]
        self.session_locks = [Lock() for _ in range(max_concurrent_requests)]
        self.crawler_lock = Lock()
        self.process_pool = Pool(processes=max_concurrent_requests)
        self.out_dir = out_dir
        self.default_id = default_id
        self.progress_bar = tqdm(unit='')
        self.downloaded_articles = 0
        self.total_links = 0
        self.url_queue, self.link2id = self.load_crawler_state(seed_links)
        
    def load_crawler_state(self, seed_links):
        log_dir = os.path.join(self.out_dir, 'logs')
        queue_loc = os.path.join(log_dir, 'queue_links.json')
        link2id_loc = os.path.join(log_dir, 'link2id.json')
        os.makedirs(os.path.join(self.out_dir, 'extracted_data'), exist_ok=True)
        if constants.SAVE_RAW_HTML:
            os.makedirs(os.path.join(self.out_dir, 'raw_data'), exist_ok=True)

        if os.path.isdir(log_dir):
            with open(queue_loc) as f:
                l = json.load(f)
            with open(link2id_loc) as f:
                d = json.load(f)
        else:
            l = []
            d = {}

        all_links = set(l + [self.base_url] + seed_links + list(d.keys()))
        q = SetQueue()

        for link in all_links:
            if link not in d or d[link] == -1 or d[link] == self.default_id:
                d.pop(link, None)
                q.put(link)
                self.total_links += 1

        return q, d

    def save_crawler_state(self, empty_queue=True):
        log_dir = os.path.join(self.out_dir, 'logs')
        queue_loc = os.path.join(log_dir, 'queue_links.json')
        link2id_loc = os.path.join(log_dir, 'link2id.json')
        
        os.makedirs(log_dir, exist_ok=True)
        
        if empty_queue:
            with open(queue_loc, 'w') as f:
                queue_links = self.serialize_queue()
                json.dump(queue_links, f, ensure_ascii=False, indent=4)

        with open(link2id_loc, 'w') as f:
            json.dump(self.link2id, f, ensure_ascii=False, indent=4)

    def serialize_queue(self):
        elements = []
        while True:
            try:
                element = self.url_queue.get(False)
                self.url_queue.task_done()
                elements.append(element)
            except Empty:
                return elements

    def update_queue(self, elements):
        self.crawler_lock.acquire()
        
        if isinstance(elements, str): 
            self.url_queue.put(elements)
        else: # assume elements is a non string iterable
            for element in elements:
                self.url_queue.put(element)

        self.total_links += 1
        self.crawler_lock.release()


    def update(self, idx):
        lock = self.session_locks[idx]
        session = self.sessions[idx]
        try:
            links, content, output_fname = self.parse_html(session)
        except:
            print(traceback.format_exc())
            links, content, output_fname = [], '', ''

        if not links and not content and not output_fname:
            try:
                session.open_new_session()
            except:
                pass
            lock.release()
            return

        self.save_data(session, links, content, output_fname)
        lock.release()

    def handle_error(self, error):
        print('error_callback:', error)

    def save_data(self, session, links, content, output_fname):
        self.crawler_lock.acquire()
        
        self.progress_bar.update()
        self.progress_bar.set_description(f'downloaded : {self.downloaded_articles}, total links: {self.total_links}, fetched links')
        
        if self.progress_bar.n and (self.progress_bar.n % constants.SAVE_CRAWLER_STATE_INTERVAL) == 0:
            self.save_crawler_state(empty_queue=False)

        if not output_fname:
            output_fname = self.default_id

        self.link2id[session.session.current_url] = output_fname

        if content and output_fname != self.default_id:
            with open(os.path.join(self.out_dir, 'extracted_data', output_fname), 'w',encoding="utf8") as f:
                print(content, file=f)
            
            if constants.SAVE_RAW_HTML:
                try:
                    html = session.session.page_source
                except:
                    html = '' 
                    
                with open(os.path.join(self.out_dir, 'raw_data', output_fname), 'w',encoding="utf8") as f:
                    print(html, file=f)
                
            self.downloaded_articles += 1
                
        for link in links:
            if link not in self.link2id:
                self.url_queue.put(link)
                self.total_links += 1

        self.crawler_lock.release()
        

    def parse_html(self, session):
        """Figure out what kind of page this is and return new links to crawl, extracted data and possible
            output file name. If both links and content are empty, it'll be considered that something
            has gone wrong and this is a signal to use a new session. If theres only one producer thread,
            you could use ```update_queue(elements)``` to enter new links in the queue as soon as they
            are encountered.
                        
        Args:
            session ([type]): [description]

        Returns:
            links   (List):     New links to crawl
            content (string):   Content extracted from this page
            output_fname (string):  output filename if this page will be saved to disk, `None` otherwise
                
        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError()


    def run(self):
        req_count = 0
        try:
            next_url = self.url_queue.get(False)
            self.url_queue.task_done()
        except Empty:
            next_url = False
            
        while next_url:
            try:
                idx = req_count % len(self.sessions)
                self.process_pool.apply_async(
                    self.request, args=(idx, next_url),
                    callback=self.update,
                    error_callback=self.handle_error
                )
                patience = 0

                while True:
                    try:
                        next_url = self.url_queue.get(timeout=15)
                        self.url_queue.task_done()
                    except Empty:
                        time.sleep(15)
                        locks = [lock for lock in self.session_locks if lock.locked()]
                        if locks:
                            continue
                        else:
                            patience += 1
                            if patience >= 4:
                                raise Empty
                            else:
                                continue
                        
                    self.crawler_lock.acquire()
                    if next_url in self.link2id:
                        self.crawler_lock.release()
                        continue
                    else:
                        self.link2id[next_url] = -1
                        req_count += 1
                        self.crawler_lock.release()
                        break

            except Empty:
                self.progress_bar.set_description(f'Exited queue loop, total links: {self.total_links}')
                break
            except:
                print(traceback.format_exc())
                self.save_crawler_state()

        try:
            self.wait_for_completion()
        except: # in case we press ctrl-c
            print(traceback.format_exc())
            self.save_crawler_state()
            self.progress_bar.close()
            for session in self.sessions:
                session.quit()

    def request(self, idx, url):
        lock = self.session_locks[idx]
        lock.acquire()
        session = self.sessions[idx]
        session.request(url)

        return idx
        
    def wait_for_completion(self):
        self.process_pool.close()
        self.process_pool.join()
        self.save_crawler_state()
        self.url_queue.join()
        self.progress_bar.close()
        for session in self.sessions:
            session.quit()
