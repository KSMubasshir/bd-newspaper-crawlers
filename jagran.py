# - * -coding: utf - 8 - * -
# encoding = utf8
import sys
from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')
import os
import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://www.jagran.com'

# for index in range(8000,8500):
for index in range(1, 9000):
    with open("log1.txt", "a") as logFile:
        logFile.write(str(index) + "\n")

    url = newspaper_base_url + "/latest-news-page" + str(index) + ".html"

    try:
        print(url)
        archive_soup = requests.get(url)
    except:
        print("No response for links in archive,passing")
        continue

    soup = BeautifulSoup(archive_soup.content, "html.parser")

    all_links = soup.find_all("a")
    page_links_length = len(all_links)

    if page_links_length == 0:
        break
    else:
        for link in all_links:
            link_separator = link.get('href')
            try:
                link_tokens = link_separator.split("/")
            except:
                continue
            if len(link_tokens) == 3 and link_tokens[2].endswith(".html"):
                article_url = newspaper_base_url + link_separator
            else:
                continue

            try:
                print(article_url)
                article_data = requests.get(article_url).text
            except:
                print("No response for content in link,trying to reconnect")
                time.sleep(2)
                continue

            article_soup = BeautifulSoup(article_data, "html.parser")

            try:
                title = article_soup.find("meta", {"name": "twitter:title"}).get('content').strip()
            except:
                title = ""

            try:
                article_content = article_soup.find("div", {"class": "articleBody"}).get_text().strip()
            except:
                article_content = ""

            data = "<article>\n"
            data += "<title>" + title + "</title>\n"
            data += "<text>\n" + article_content + "\n</text>\n"
            data += "</article>"

            output_file_name = link_tokens[2]

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
                with open(raw_output_dir + '/' + output_file_name, 'w') as file:
                    file.write(str(article_soup))
            except:
                pass

            try:
                with open(output_dir + '/' + output_file_name, 'w') as file:
                    file.write(data)
            except:
                pass
