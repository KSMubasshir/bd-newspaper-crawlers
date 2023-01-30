# -*- coding: utf-8 -*-
# encoding=utf8
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

newspaper_base_url = 'http://www.dainikamadershomoy.com/'

for index in range(20000):
    with open("log.txt", "a") as logFile:
        logFile.write(str(index) + "\n")
        url = newspaper_base_url + 'archive/all/' + str(index * 20)
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
                if len(link_tokens) == 5 and link_tokens[4].isnumeric():
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
                    title = article_soup.find("title").get_text().split("–")[0].strip()
                except:
                    title = ""

                try:
                    author = article_soup.find("span", {"class": "w3-black"}).get_text().strip()
                except:
                    author = ""

                try:
                    date = article_soup.find("div", {"class": "w3-col l8"}).get_text().strip()
                    date_tokens = date.split(" ")
                    author_length = len(author.split(" "))
                    date = date_tokens[author_length + 1] + " " + date_tokens[author_length + 2] + " " + date_tokens[
                        author_length + 3]
                    date = date.strip()
                except:
                    date = ""

                try:
                    paragraphs = article_soup.find_all("p")
                    article_content = ""
                    for para in paragraphs:
                        article_content += para.get_text().strip() + " "
                    article_content = article_content.replace("সব খবর", "")
                    article_content = article_content.replace(
                        "© সর্বস্বত্ব স্বত্বাধিকার সংরক্ষিত ২০০০-২০১৯  Privacy Policy", "")
                    article_content = article_content.strip()
                except:
                    article_content = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<author>" + author + "</author>\n"
                data += "<date>" + date + "</date>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[4]

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
