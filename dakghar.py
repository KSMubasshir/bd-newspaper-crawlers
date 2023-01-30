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


newspaper_base_url = 'https://www.dakghar24.com/'

for index in range(89, 100):
    # for index in range( 165 , 200 ):
    for j in range(13):
        if j == 0:
            url = newspaper_base_url + "our-home/page/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "foreign-home/page/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "game-home/page/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "international-home/page/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "politics-home/page/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "entertainment-home/page/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "education-home/page/" + str(index)
        elif j == 7:
            url = newspaper_base_url + "decor-home/page/" + str(index)
        elif j == 8:
            url = newspaper_base_url + "literary-home/page/" + str(index)
        elif j == 9:
            url = newspaper_base_url + "readers-home/page/" + str(index)
        elif j == 10:
            url = newspaper_base_url + "technology-home/page/" + str(index)
        elif j == 11:
            url = newspaper_base_url + "picture-home/page/" + str(index)
        elif j == 12:
            url = newspaper_base_url + "video-home/page/" + str(index)

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
                if len(link_tokens) == 3:
                    if "home" in link_tokens[1]:
                        continue
                    article_url = newspaper_base_url + link_tokens[1]
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

                output_file_name = link_tokens[1]

                output_dir = './{}/{}/{}/bn'.format(year, month, day)
                raw_output_dir = "../Raw/Dakghar24/" + output_dir

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
