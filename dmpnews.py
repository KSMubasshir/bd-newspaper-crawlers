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

newspaper_base_url = 'https://dmpnews.org'
newspaper_archive_base_url = 'https://dmpnews.org'

start_date = date(2020, 10, 31)
end_date = date.today()
delta = end_date - start_date
output_result = []
data = []
exceptions = 0


def month_converter(month):
    if month == "জানুয়ারী":
        month = 1
    elif month == "ফেব্রুয়ারী":
        month = 2
    elif month == "মার্চ":
        month = 3
    elif month == "এপ্রিল":
        month = 4
    elif month == "মে":
        month = 5
    elif month == "জুন":
        month = 6
    elif month == "জুলাই":
        month = 7
    elif month == "আগস্ট":
        month = 8
    elif month == "সেপ্টেম্বর":
        month = 9
    elif month == "অক্টোবর":
        month = 10
    elif month == "নভেম্বর":
        month = 11
    else:
        month = 12

    return month


def date_translator(bn_number):
    en_number = ""
    for letter in bn_number:
        if letter == '০':
            en_number += "0"
        elif letter == '১':
            en_number += "1"
        elif letter == '২':
            en_number += "2"
        elif letter == '৩':
            en_number += "3"
        elif letter == '৪':
            en_number += "4"
        elif letter == '৫':
            en_number += "5"
        elif letter == '৬':
            en_number += "6"
        elif letter == '৭':
            en_number += "7"
        elif letter == '৮':
            en_number += "8"
        elif letter == '৯':
            en_number += "9"

    return en_number


for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    print(date_str)
    with open("log.txt", 'a') as file:
        file.write(str(date_str) + '\n')
    for i in range(1, 10):
        url = newspaper_archive_base_url + "/" + str(date_str.year) + "/" + str(date_str.month) + "/" + str(
            date_str.day) + "/page/" + str(i)
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
                    article_url = link.get('href')
                    link_separator = article_url.split('/')
                except:
                    continue
                if len(link_separator) != 5 or "dmpnews.org" not in link_separator[2]:
                    continue
                output_file_name = '{}.txt'.format(link_separator[3])
                try:
                    article_data = requests.get(article_url).text
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue
                article_soup = BeautifulSoup(article_data, "html.parser")

                print(article_url)

                try:
                    date_published = article_soup.find("time", {"itemprop": "datePublished"}).get_text().strip()
                except Exception as e:
                    continue

                try:
                    article_title_text = article_soup.find("title").get_text().split("|")[0].strip()
                except:
                    article_title_text = ""

                try:
                    article_body_text = article_soup.find("div", {"class": "entry-content"}).get_text().replace(
                        "printশেয়ার করুনTweetEmail", "").strip()
                except:
                    article_body_text = ""

                try:
                    article_body_text = article_body_text.replace("ডিএমপি নিউজ রিপোর্ট:", "").strip()
                except:
                    pass
                try:
                    article_body_text = article_body_text.replace("ডিএমপি নিউজঃ", "").strip()
                except:
                    pass
                try:
                    article_body_text = article_body_text.replace("ডিএমপি নিউজ:", "").strip()
                except:
                    pass
                try:
                    article_body_text = article_body_text.replace("Categories:", "").strip()
                except:
                    pass
                try:
                    article_body_text = article_body_text.replace("ডিএমপি ‍নিউজ রিপোর্ট:", "").strip()
                except:
                    pass

                data = "<article>\n"
                data += "<title>" + article_title_text + "</title>\n"
                data += "<date>" + date_published + "</date>\n"
                data += "<text>" + "\n" + article_body_text + "\n" + "</text>\n"
                data += "</article>"

                with open('Raw/' + output_file_name, 'w') as file:
                    file.write(str(article_url) + '\n' + str(article_data))
                with open('Data/' + output_file_name, 'w') as file:
                    file.write(data + '\n\n')
