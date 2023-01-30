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

newspaper_base_url = 'https://hindime.net'
ignore_list = ["keyword", "micr-code", "swift-code", "pin-code", "tech", "internet", "blogging", "seo",
               "make-money-online", "cryptocurrency", "share-market", "wiki", "privacy-policy", "keyword", "about",
               "contact"]

for index in range(1, 18):
    with open("log.txt", "a") as logFile:
        logFile.write(str(index) + "\n")

        for j in range(8):
            if j == 0:
                url = newspaper_base_url + '/internet/page/' + str(index)
            if j == 1:
                url = newspaper_base_url + '/blogging/page/' + str(index)
            if j == 2:
                url = newspaper_base_url + '/seo/page/' + str(index)
            if j == 3:
                url = newspaper_base_url + '/cryptocurrency/page/' + str(index)
            if j == 4:
                url = newspaper_base_url + '/computer/page/' + str(index)
            if j == 5:
                url = newspaper_base_url + '/share-market/page/' + str(index)
            if j == 6:
                url = newspaper_base_url + '/tech/page/' + str(index)
            if j == 7:
                url = newspaper_base_url + '/make-money-online/page/' + str(index)

            try:
                print(url)
                archive_soup = requests.get(url)
            except:
                print("No response for links in archive,passing")
                continue

            soup = BeautifulSoup(archive_soup.content, "html.parser")

            all_links = soup.find_all("a")
            page_links_length = len(all_links)

            if (page_links_length == 0):
                break
            else:
                for link in all_links:
                    link_separator = link.get('href')
                    try:
                        link_tokens = link_separator.split("/")
                    except:
                        continue
                    if len(link_tokens) == 5 and "hindime.net" in link_tokens[2]:
                        if link_tokens[3] in ignore_list:
                            continue
                        article_url = link_separator
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
                        title = article_soup.find("h1", {"class": "entry-title"}).get_text().strip()
                    except:
                        title = ""

                    try:
                        article_content = article_soup.find("div",
                                                            {"class": "td-post-content tagdiv-type"}).get_text().strip()

                    except:
                        article_content = ""

                    data = "<article>\n"
                    data += "<title>" + title + "</title>\n"
                    data += "<text>\n" + article_content + "\n</text>\n"
                    data += "</article>"

                    output_file_name = link_tokens[3]

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
