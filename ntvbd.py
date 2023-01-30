# -*- coding: utf-8 -*-
# encoding=utf8
import sys
from importlib import reload

reload(sys)
sys.setdefaultencoding('utf8')
import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://www.ntvbd.com'
newspaper_archive_base_url = 'https://www.ntvbd.com/archive'

# start_date = date(2020, 6, 1)
start_date = date(2019, 10, 26)
end_date = date.today()
delta = end_date - start_date
output_result = []
data = []
exceptions = 0

for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    print(date_str)
    with open("log.txt", 'a') as file:
        file.write(str(date_str) + '\n')
    output_dir = './{}/{}/{}/bn'.format(date_str.year, date_str.month, date_str.day)
    raw_output_dir = './' + "Raw" + '/' + output_dir
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass

    url = newspaper_archive_base_url + "/" + str(date_str.year) + "/" + str(date_str.month) + "/" + str(date_str.day)
    try:
        print(url)
        archive_soup = requests.get(url)
    except:
        print("No response for links in archive,trying to reconnect")
        time.sleep(2)
        continue
    soup = BeautifulSoup(archive_soup.content, "html.parser")

    all_links = soup.find_all("a")
    page_links_length = len(all_links)

    if page_links_length == 0:
        break
    else:
        for link in all_links:
            try:
                link_separator = link.get('href').split('/')
            except:
                continue
            if len(link_separator) != 4:
                continue
            if "ntvbd.com" in link_separator[2] or "facebook.com" in link_separator[2] or "twitter.com" in \
                    link_separator[2]:
                continue
            link = "/" + link_separator[1] + "/" + link_separator[2] + "/" + link_separator[3]
            output_file_name = 'bn_{}{}.txt'.format(link_separator[1], link_separator[2])
            article_url = newspaper_base_url + link
            try:
                article_data = requests.get(article_url).text
            except:
                print("No response for content in link,trying to reconnect")
                time.sleep(2)
                continue
            with open(raw_output_dir + '/' + output_file_name, 'w') as file:
                file.write(str(article_url) + '\n' + str(article_data))
            article_soup = BeautifulSoup(article_data, "html.parser")

            print(article_url)

            try:
                author = article_soup.find("div", {"class": "author-section pt-20 clearfix"}).get_text().strip()
            except Exception as e:
                print(e)
                author = ""

            try:
                date_published = article_soup.find("div", {"class": "date color-gray"}).get_text().strip()
            except:
                date_published = ""

            try:
                article_title_text = article_soup.find("h1", {"itemprop": "headline"}).get_text()
            except:
                article_title_text = ""
            try:
                article_body_text = article_soup.find("div", {
                    "class": "section-content pl-30 pr-30 pb-20 text-justify"}).get_text().strip()
            except:
                article_body_text = ""

            data = "<article>\n"
            data += "<title>" + article_title_text + "</title>\n"
            data += "<date>" + date_published + "</date>\n"
            data += "<author>" + author + "</author>\n"
            data += "<text>" + "\n" + article_body_text + "\n" + "</text>\n"
            data += "</article>"

            with open(output_dir + '/' + output_file_name, 'w') as file:
                file.write(data + '\n\n')
