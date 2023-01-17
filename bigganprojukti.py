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


newspaper_base_url = 'http://www.bigganprojukti.com/'
# 51
for index in range(13, 14):
    for j in range(23, 38):
        if j == 0:
            url = newspaper_base_url + "category/" + "news" + "/page/" + str(index)
        if j == 1:
            url = newspaper_base_url + "category/" + "news/টুকরো-খবর" + "/page/" + str(index)
        if j == 2:
            url = newspaper_base_url + "category/" + "news/localnews" + "/page/" + str(index)
        if j == 3:
            url = newspaper_base_url + "category/" + "news/newproducts" + "/page/" + str(index)
        if j == 4:
            url = newspaper_base_url + "category/" + "news/technologyworld" + "/page/" + str(index)
        if j == 5:
            url = newspaper_base_url + "category/" + "সৌর-জগৎ" + "/page/" + str(index)
        if j == 6:
            url = newspaper_base_url + "category/" + "physics" + "/page/" + str(index)
        if j == 7:
            url = newspaper_base_url + "category/" + "chemistry" + "/page/" + str(index)
        if j == 8:
            url = newspaper_base_url + "category/" + "mathematics" + "/page/" + str(index)
        if j == 9:
            url = newspaper_base_url + "category/" + "animals" + "/page/" + str(index)
        if j == 10:
            url = newspaper_base_url + "category/" + "পৃথিবী-ও-পরিবেশ" + "/page/" + str(index)
        if j == 11:
            url = newspaper_base_url + "category/" + "electronics" + "/page/" + str(index)
        if j == 12:
            url = newspaper_base_url + "category/" + "science-fiction" + "/page/" + str(index)
        if j == 13:
            url = newspaper_base_url + "category/" + "hardware" + "/page/" + str(index)
        if j == 14:
            url = newspaper_base_url + "category/" + "software" + "/page/" + str(index)
        if j == 15:
            url = newspaper_base_url + "category/" + "internet" + "/page/" + str(index)
        if j == 16:
            url = newspaper_base_url + "category/" + "operating-system" + "/page/" + str(index)
        if j == 17:
            url = newspaper_base_url + "category/" + "programming" + "/page/" + str(index)
        if j == 18:
            url = newspaper_base_url + "category/" + "open-source" + "/page/" + str(index)
        if j == 19:
            url = newspaper_base_url + "category/" + "bangla-computing" + "/page/" + str(index)
        if j == 20:
            url = newspaper_base_url + "category/" + "download" + "/page/" + str(index)
        if j == 21:
            url = newspaper_base_url + "category/" + "social-media" + "/page/" + str(index)
        if j == 22:
            url = newspaper_base_url + "category/" + "graphics-design" + "/page/" + str(index)
        if j == 23:
            url = newspaper_base_url + "category/" + "web-design" + "/page/" + str(index)
        if j == 24:
            url = newspaper_base_url + "category/" + "web-development" + "/page/" + str(index)
        if j == 25:
            url = newspaper_base_url + "category/" + "wordpress" + "/page/" + str(index)
        if j == 26:
            url = newspaper_base_url + "category/" + "video-editing" + "/page/" + str(index)
        if j == 27:
            url = newspaper_base_url + "category/" + "freelancing/এসইও" + "/page/" + str(index)
        if j == 28:
            url = newspaper_base_url + "category/" + "tips" + "/page/" + str(index)
        if j == 29:
            url = newspaper_base_url + "category/" + "freelancing" + "/page/" + str(index)
        if j == 30:
            url = newspaper_base_url + "category/" + "অনলাইনে-আয়" + "/page/" + str(index)
        if j == 31:
            url = newspaper_base_url + "category/" + "web-review" + "/page/" + str(index)
        if j == 32:
            url = newspaper_base_url + "category/" + "game-review" + "/page/" + str(index)
        if j == 33:
            url = newspaper_base_url + "category/" + "mobile-phone" + "/page/" + str(index)
        if j == 34:
            url = newspaper_base_url + "category/" + "sci-tech-news" + "/page/" + str(index)
        if j == 35:
            url = newspaper_base_url + "category/" + "report" + "/page/" + str(index)
        if j == 36:
            url = newspaper_base_url + "category/" + "interview-desk" + "/page/" + str(index)
        if j == 37:
            url = newspaper_base_url + "category/" + "photo-blog" + "/page/" + str(index)

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
                if len(link_tokens) == 5 and link_tokens[2] == "www.bigganprojukti.com":
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
                    title = article_soup.find("h1", {"class", "entry-title"}).get_text().split("-")[0].strip()
                except:
                    try:
                        title = article_soup.find("h1", {"class", "entry-title"}).get_text().strip()
                    except:
                        title = ""
                try:
                    article_content = article_soup.find("div", {"class": "td-post-content"}).get_text().strip()
                except:
                    article_content = ""
                try:
                    author = article_soup.find("span", {"class": "td-post-author-name"}).get_text().strip()
                except:
                    author = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<author>" + author + "</author>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[3]

                output_dir = './Data'
                raw_output_dir = "./Raw"

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
