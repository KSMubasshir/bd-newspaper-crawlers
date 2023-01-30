import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests


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


newspaper_base_url = 'https://bangla.hindustantimes.com/'

for index in range(1, 300):
    for j in range(6):
        if j == 0:
            url = newspaper_base_url + "nation-and-world" + "/page-" + str(index)
        if j == 1:
            url = newspaper_base_url + "topic/amphan" + "/page-" + str(index)
        if j == 2:
            url = newspaper_base_url + "bengal" + "/page-" + str(index)
        if j == 3:
            url = newspaper_base_url + "sports" + "/page-" + str(index)
        if j == 4:
            url = newspaper_base_url + "entertainment" + "/page-" + str(index)
        if j == 5:
            url = newspaper_base_url + "astrology" + "/page-" + str(index)
        if j == 6:
            url = newspaper_base_url + "career" + "/page-" + str(index)
        if j == 7:
            url = newspaper_base_url + "brief-news" + "/page-" + str(index)
        if j == 8:
            url = newspaper_base_url + "latest-news" + "/page-" + str(index)

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
                if len(link_tokens) == 3 and (".htm" in link_tokens[2]):
                    article_url = newspaper_base_url + link_separator[1:]
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
                    title = article_soup.find("title").get_text()
                    title = title.replace(", Bangla News", "")
                except:
                    title = ""
                try:
                    article_content = article_soup.find("div", {"class": "mainArea"}).get_text()
                    article_content = article_content.replace("শেয়ার করুন", "")
                except:
                    article_content = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[2][:len(link_tokens[2]) - 4]

                output_dir = './Data'
                raw_output_dir = "./Raw/"

                try:
                    os.makedirs(output_dir)
                except OSError:
                    pass
                try:
                    os.makedirs(raw_output_dir)
                except OSError:
                    pass

                try:
                    with open(raw_output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                        file.write(str(article_soup))
                except:
                    pass

                try:
                    with open(output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                        file.write(data)
                except:
                    pass
