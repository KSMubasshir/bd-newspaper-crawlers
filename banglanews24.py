#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://www.banglanews24.com/'

for index in range(1, 25000):
    for j in range(31):
        if j == 0:
            url = newspaper_base_url + "category/জাতীয়/1?page=" + str(index)
        elif j == 1:
            url = newspaper_base_url + "category/রাজনীতি/2?page=" + str(index)
        elif j == 2:
            url = newspaper_base_url + "category/অর্থনীতি/3?page=" + str(index)
        elif j == 3:
            url = newspaper_base_url + "category/আন্তর্জাতিক/4?page=" + str(index)
        elif j == 4:
            url = newspaper_base_url + "category/খেলা/5?page=" + str(index)
        elif j == 5:
            url = newspaper_base_url + "category/বিনোদন/6?page=" + str(index)
        elif j == 6:
            url = newspaper_base_url + "category/তথ্যপ্রযুক্তি/7?page=" + str(index)
        elif j == 7:
            url = newspaper_base_url + "category/শিল্প-সাহিত্য/11?page=" + str(index)
        elif j == 8:
            url = newspaper_base_url + "category/লাইফস্টাইল/12?page=" + str(index)
        elif j == 9:
            url = newspaper_base_url + "/category/পর্যটন/13?page=" + str(index)
        elif j == 10:
            url = newspaper_base_url + "/category/চট্টগ্রাম-প্রতিদিন/14?page=" + str(index)
        elif j == 11:
            url = newspaper_base_url + "category/আইন-আদালত/18?page=" + str(index)
        elif j == 12:
            url = newspaper_base_url + "category/ইচ্ছেঘুড়ি/8?page=" + str(index)
        elif j == 13:
            url = newspaper_base_url + "category/প্রবাস/17?page=" + str(index)
        elif j == 14:
            url = newspaper_base_url + "category/স্বাস্থ্য/19?page=" + str(index)
        elif j == 15:
            url = newspaper_base_url + "category/শিক্ষা/20?page=" + str(index)
        elif j == 16:
            url = newspaper_base_url + "category/ইসলাম/15?page=" + str(index)
        elif j == 18:
            url = newspaper_base_url + "category/মুক্তমত/16?page=" + str(index)
        elif j == 19:
            url = newspaper_base_url + "category/জলবায়ু-পরিবেশ/21?page=" + str(index)
        elif j == 20:
            url = newspaper_base_url + "category/কলকাতা/22?page=" + str(index)
        elif j == 21:
            url = newspaper_base_url + "category/ত্রিপুরা/38?page=" + str(index)
        elif j == 22:
            url = newspaper_base_url + "category/অফবিট/34?page=" + str(index)
        elif j == 23:
            url = newspaper_base_url + "news-Sort-By-District?division=2&district=1&page=" + str(index)
        elif j == 24:
            url = newspaper_base_url + "news-Sort-By-District?division=3&district=1&page=" + str(index)
        elif j == 25:
            url = newspaper_base_url + "news-Sort-By-District?division=4&district=1&page=" + str(index)
        elif j == 26:
            url = newspaper_base_url + "news-Sort-By-District?division=5&district=1&page=" + str(index)
        elif j == 27:
            url = newspaper_base_url + "news-Sort-By-District?division=6&district=1&page=" + str(index)
        elif j == 28:
            url = newspaper_base_url + "news-Sort-By-District?division=7&district=1&page=" + str(index)
        elif j == 29:
            url = newspaper_base_url + "news-Sort-By-District?division=8&district=1&page=" + str(index)
        elif j == 30:
            url = newspaper_base_url + "news-Sort-By-District?division=9&district=1&page=" + str(index)

        print(url)

        try:
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
                if len(link_tokens) == 7:
                    if link_tokens[4] == "news" and link_tokens[5] == "bd":
                        article_url = link_separator
                        print(article_url)
                    else:
                        continue
                else:
                    continue

                try:
                    article_data = requests.get(article_url).text
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue

                article_soup = BeautifulSoup(article_data, "html.parser")
                paragraphs = article_soup.find_all("p")
                title = article_soup.find("title").get_text()
                date_time = article_soup.find("meta", {"name": "publish-date"})
                date = date_time.get('content').split(" ")[1]
                splitted_date = date.split("-")

                author = article_soup.find_all("span")[12].get_text()

                year = splitted_date[0]
                month = splitted_date[1]
                day = splitted_date[2]

                length = len(paragraphs)
                length = length - 1

                i = 0

                article_content = ""
                for paragraph in paragraphs:
                    if i == 0:
                        pass
                    elif i == 1:
                        try:
                            article_content += paragraph.get_text().split(":")[1][1:] + "\n"
                        except:
                            article_content += paragraph.get_text() + "\n"
                    elif i <= length - 2:
                        article_content += paragraph.get_text() + "\n"
                    else:
                        pass
                    i = i + 1

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                # data +=  "<date>" + date + "</date>\n"
                data += "<text>\n" + article_content + "</text>\n"
                data += "</article>"

                output_file_name = link_tokens[3] + "_" + link_tokens[4] + "_" + link_tokens[5] + "_" + link_tokens[6]
                output_dir = './{}/{}/{}/bn'.format(year, month, day)
                raw_output_dir = '../' + "Raw" + '/' + "Banglanews24" + '/' + output_dir

                try:
                    os.makedirs(output_dir)
                except OSError:
                    pass
                try:
                    os.makedirs(raw_output_dir)
                except OSError:
                    pass

                with open(output_dir + '/raw_' + output_file_name, 'w') as file:
                    file.write(article_soup.encode('utf-8'))

                with open(output_dir + '/' + output_file_name, 'w') as file:
                    file.write(data.encode('utf-8'))
