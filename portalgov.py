# - * -coding: utf - 8 - * -
# encoding = utf8
import sys
from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')
import json
import time
import difflib
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import os
from datetime import date, timedelta
import time

link_set = set()
visited = set()
count = 0


def loadLinks():
    global link_set
    global visited
    with open('all.txt', 'r') as file1:
        with open('visited.txt', 'r') as file2:
            visited = set(file2)
            link_set = set(file1).difference(file2)


def extract_data(article_soup, output_file_name):
    try:
        article_content = ""
        paragraphs = article_soup.find_all("p", {"style": "text-align:justify"})
        listitems = article_soup.find_all("li", {"style": "text-align:justify"})
        for para in paragraphs:
            article_content += para.get_text().strip() + "\n"
        for li in listitems:
            article_content += li.get_text().strip() + "\n"
    except:
        article_content = ""

    data = "<article>\n"
    data += "<text>\n" + article_content + "\n</text>\n"
    data += "</article>"

    output_dir = './Data/'
    raw_output_dir = './' + "Raw" + '/'

    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass

    try:
        with open(raw_output_dir + '/' + str(output_file_name), 'w') as file:
            file.write(str(article_soup))
    except Exception as e:
        print(e)
        pass

    if len(paragraphs) == 0 and len(listitems) == 0:
        return
    try:
        with open(output_dir + '/' + str(output_file_name), 'w') as file:
            file.write(data)
    except Exception as e:
        print(e)
        pass


def start():
    base_url = 'http://dae.gov.bd'
    try:
        print(base_url)
        article_soup = requests.get(base_url)
        soup = BeautifulSoup(article_soup.content, "html.parser")
        visited.add(base_url)
        with open("visited.txt", "a") as visited_file:
            visited_file.write(base_url + "\n")
    except Exception as e:
        print(e)
        exit()

    all_links = soup.find_all("a")

    if len(all_links) == 0:
        exit()
    else:
        for link in all_links:
            lnk = link.get('href')
            if lnk.startswith("/site"):
                lnk = "http://dae.portal.gov.bd" + lnk
            elif "http://dae.portal.gov.bd" in lnk:
                pass
            else:
                continue
            link_set.add(lnk)
            with open("all.txt", "a") as all_file:
                all_file.write(lnk + "\n")

    restart()


def restart():
    global link_set
    while len(link_set) > 0:
        global count
        url = link_set.pop()
        if url.startswith("/site"):
            url = "http://dae.portal.gov.bd" + url
        elif "http://dae.portal.gov.bd" in url:
            pass
        else:
            continue
        visited.add(url)
        with open("visited.txt", "a") as visited_file:
            visited_file.write(url + "\n")
        soup = requests.get(url)

        article_soup = BeautifulSoup(soup.content, "html.parser")

        print(url)
        extract_data(article_soup, count)
        count = count + 1
        new_links = article_soup.find_all("a")
        if len(new_links) == 0:
            pass
        else:
            for full_link in new_links:
                link = full_link.get('href')
                if link in visited:
                    continue
                link_set.add(link)
                with open("all.txt", "a") as all_file:
                    all_file.write(link + "\n")


if __name__ == '__main__':
    # start()
    loadLinks()
    restart()
