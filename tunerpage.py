import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests


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


newspaper_base_url = 'https://tunerpage.com/'

for index in range(1, 100):
    for j in range(41):
        if j == 0:
            url = newspaper_base_url + "off-topic/e-book/page/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "internet-news/page/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "electronics/page/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "উইন্ডোজ/page/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "উইন্ডোজ-৭/page/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "important-computer-tricks/page/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "anti-virus-free/page/" + str(index)
        elif j == 7:
            url = newspaper_base_url + "android/page/" + str(index)
        elif j == 8:
            url = newspaper_base_url + "wordpress-and-joomla-tricks/page/" + str(index)
        elif j == 9:
            url = newspaper_base_url + "web-designing/page/" + str(index)
        elif j == 10:
            url = newspaper_base_url + "কম্পিউটার/page/" + str(index)
        elif j == 11:
            url = newspaper_base_url + "how-to/page/" + str(index)
        elif j == 12:
            url = newspaper_base_url + "quiz/page/" + str(index)
        elif j == 13:
            url = newspaper_base_url + "গুগল/page/" + str(index)
        elif j == 14:
            url = newspaper_base_url + "graphics-designing/page/" + str(index)
        elif j == 15:
            url = newspaper_base_url + "tutorials/page/" + str(index)
        elif j == 16:
            url = newspaper_base_url + "computer-tricks/page/" + str(index)
        elif j == 17:
            url = newspaper_base_url + "টেক-আপডেট/page/" + str(index)
        elif j == 18:
            url = newspaper_base_url + "off-topic/freedownload/page/" + str(index)
        elif j == 19:
            url = newspaper_base_url + "tunerpage-notice/page/" + str(index)
        elif j == 20:
            url = newspaper_base_url + "গেমস/page/" + str(index)
        elif j == 21:
            url = newspaper_base_url + "pendrive-tips/page/" + str(index)
        elif j == 22:
            url = newspaper_base_url + "articles/page/" + str(index)
        elif j == 23:
            url = newspaper_base_url + "programming/page/" + str(index)
        elif j == 24:
            url = newspaper_base_url + "ফরেক্স/page/" + str(index)
        elif j == 25:
            url = newspaper_base_url + "facebook/page/" + str(index)
        elif j == 26:
            url = newspaper_base_url + "freelancing/page/" + str(index)
        elif j == 27:
            url = newspaper_base_url + "latest-technology-news/page/" + str(index)
        elif j == 28:
            url = newspaper_base_url + "free-advertisement/page/" + str(index)
        elif j == 29:
            url = newspaper_base_url + "ভিডিও-টিউটোরিয়াল/page/" + str(index)
        elif j == 30:
            url = newspaper_base_url + "bangla-magazine/page/" + str(index)
        elif j == 31:
            url = newspaper_base_url + "off-topic/movie/page/" + str(index)
        elif j == 32:
            url = newspaper_base_url + "mobile-tricks-tips/page/" + str(index)
        elif j == 33:
            url = newspaper_base_url + "রহস্যময়-জগত/page/" + str(index)
        elif j == 34:
            url = newspaper_base_url + "review/page/" + str(index)
        elif j == 35:
            url = newspaper_base_url + "off-topic/সফটওয়্যার/page/" + str(index)
        elif j == 36:
            url = newspaper_base_url + "science-technology/page/" + str(index)
        elif j == 37:
            url = newspaper_base_url + "off-topic/need-help/page/" + str(index)
        elif j == 38:
            url = newspaper_base_url + "হ্যাকিং/page/" + str(index)
        elif j == 39:
            url = newspaper_base_url + "hacking-tricks/page/" + str(index)
        elif j == 40:
            url = newspaper_base_url + "seo-এসইও/page/" + str(index)

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
                if len(link_tokens) == 5 and link_tokens[3] == "archives":
                    if "respond" in link_tokens[4] or "comments" in link_tokens[4]:
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
                    date = article_soup.find("div", {"class": "jeg_meta_date"}).get_text().strip()
                    date_tokens = date.split("/")

                    day = date_translator(date_tokens[0])
                    month = date_translator(date_tokens[1])
                    year = date_translator(date_tokens[2])

                except:
                    date = "০১/০১/২০০০"
                    day = "01"
                    month = "01"
                    year = "2000"
                try:
                    title = article_soup.find("title").get_text().split("|")[0].strip()
                    title = title.split("–")[0].strip()
                except:
                    title = ""
                try:
                    article_content = article_soup.find("div", {"class": "content-inner"}).get_text().strip()
                except:
                    article_content = ""
                try:
                    author = article_soup.find("div", {"class": "jeg_meta_author"}).get_text().strip()
                except:
                    author = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<date>" + date + "</date>\n"
                data += "<author>" + author + "</author>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[4]

                output_dir = './{}/{}/{}/bn'.format(year, month, day)
                raw_output_dir = "./Raw/Tunerpage/" + output_dir

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
