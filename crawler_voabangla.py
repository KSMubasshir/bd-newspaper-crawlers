import time
import os
import re
import pickle
import json
import copy
import shutil
import constants
import traceback
import hashlib
from urllib.parse import unquote
from tqdm import tqdm
from bs4 import BeautifulSoup
from crawler_base import CrawlerBase
from sessions import TouchVPNSession
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class CrawlerVoabangla(CrawlerBase):
    def __init__(self):
        super(CrawlerVoabangla, self).__init__('https://www.voabangla.com',
                                               out_dir='voabangla',
                                               session_class=TouchVPNSession,
                                               **constants.TouchVPNSessionDefaults)
        self.blackList = set(['https://www.voabangla.com/search?q='])

    def load_full_page(self, session, patience=1):
        scrolling_js = '''window.scrollTo(0, document.body.scrollHeight);'''
        height_js = '''var l=document.body.scrollHeight; return l;'''
        prev_height = -1
        current_height = session.session.execute_script(height_js)
        current = 0

        while True:
            session.session.execute_script(scrolling_js)
            time.sleep(1)

            modal_button = EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='webPushModal']//button[@class='close']")
            )
            try:
                if modal_button(session.session):
                    session.session.find_element_by_xpath("//div[@id='webPushModal']//button[@class='close']").click()
            except:
                pass

            prev_height = current_height
            current_height = session.session.execute_script(height_js)

            if prev_height == current_height:
                current += 1
                if current >= patience:
                    break
            else:
                current = 0

    def parse_html(self, session):
        links = set()
        content = ''
        output_fname = ''

        article_page = False

        if session.session.current_url.startswith('https://www.voabangla.com') and len(
                session.session.current_url.split("/")) == 6:
            article_page = True
            patience = 1
        else:
            patience = 2

        self.load_full_page(session, patience)

        soup = BeautifulSoup(session.session.page_source, 'html.parser')
        if session.session.current_url.startswith('https://www.voabangla.com'):
            links.add(session.session.current_url)

            for link in soup.find_all('a', href=True):
                extension = link['href']
                if extension.startswith('/'):
                    actual_link = 'https://www.voabangla.com' + extension
                elif extension.startswith('https://www.voabangla.com'):
                    actual_link = extension
                else:
                    actual_link = ''

                if actual_link and actual_link not in self.blackList:
                    links.add(actual_link)

        else:
            links.add('https://www.voabangla.com')

        if article_page:
            soup = soup.find("div", {"id": "content"})
            if soup:

                title_element = soup.find("h1", {"class": "title pg-title"})
                if title_element:
                    title_text = title_element.get_text()
                else:
                    title_text = ''

                content_element = soup.find("div", {"id": "article-content"})
                if content_element:
                    content_text = content_element.get_text()
                else:
                    content_text = ''

                if title_text and content_text:
                    content = f'''
                    <article>
                    <title>{title_text}</title>
                    <text>
                    {content_text}
                    </text>
                    </article>
                    '''
                    encoded_link = unquote(session.session.current_url).encode('utf-8', errors='ignore')
                    h = hashlib.sha1()
                    h.update(encoded_link)
                    output_fname = h.hexdigest()

        return links, content, output_fname


if __name__ == "__main__":
    crawler = CrawlerVoabangla()
    crawler.run()
