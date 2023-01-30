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


newspaper_base_url = 'http://www.sasthabangla.com/'

for index in range(100):
    for j in range(33):
        if j == 0:
            url = newspaper_base_url + "category/health-news/দেশী-সংবাদ/page/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "category/health-news/বিদেশি-সংবাদ/page/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "category/pregnancy/women-health/page/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "category/pregnancy/page/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "category/pregnancy/health-and-illness-in-pregnancy/page/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "category/pregnancy/signs-of-pregnancy/page/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "category/pregnancy/জন্ম-নিয়ন্ত্রন/page/" + str(index)
        elif j == 7:
            url = newspaper_base_url + "category/pregnancy/বিবিধ/page/" + str(index)
        elif j == 8:
            url = newspaper_base_url + "category/diseases/kidnie/page/" + str(index)
        elif j == 9:
            url = newspaper_base_url + "category/diseases/চর্মরোগ/page/" + str(index)
        elif j == 10:
            url = newspaper_base_url + "/category/diseases/eye-problem/page/" + str(index)
        elif j == 11:
            url = newspaper_base_url + "category/diseases/dental-problem/page/" + str(index)
        elif j == 12:
            url = newspaper_base_url + "category/diseases/নাককানগলা/page/" + str(index)
        elif j == 13:
            url = newspaper_base_url + "category/diseases/নিউরো-সমস্যা/page/" + str(index)
        elif j == 14:
            url = newspaper_base_url + "category/diseases/intestine-problems/page/" + str(index)
        elif j == 15:
            url = newspaper_base_url + "category/diseases/health-problems-men/page/" + str(index)
        elif j == 16:
            url = newspaper_base_url + "category/diseases/ফুসফুসের-সমস্যা/page/" + str(index)
        elif j == 17:
            url = newspaper_base_url + "category/diseases/mental-illness/page/" + str(index)
        elif j == 18:
            url = newspaper_base_url + "category/diseases/মেয়েলী-সমস্যা-সমূহ/page/" + str(index)
        elif j == 19:
            url = newspaper_base_url + "category/diseases/রক্তনালীর-সমস্যা/page/" + str(index)
        elif j == 20:
            url = newspaper_base_url + "category/diseases/লিভারযকৃৎ-এর-সমস্যা/page/" + str(index)
        elif j == 21:
            url = newspaper_base_url + "category/diseases/infectious-disease/page/" + str(index)
        elif j == 22:
            url = newspaper_base_url + "category/diseases/hormonal-problems/page/" + str(index)
        elif j == 23:
            url = newspaper_base_url + "category/diseases/orthopaedic-conditions/page/" + str(index)
        elif j == 24:
            url = newspaper_base_url + "category/diseases/heart-diseases/page/" + str(index)
        elif j == 25:
            url = newspaper_base_url + "category/health-technology/country-health-technology/page/" + str(index)
        elif j == 26:
            url = newspaper_base_url + "category/health-technology/international-health-technology/page/" + str(index)
        elif j == 27:
            url = newspaper_base_url + "category/tips/ফিটনেস-টিপস/page/" + str(index)
        elif j == 28:
            url = newspaper_base_url + "category/tips/beauty-tips/page/" + str(index)
        elif j == 29:
            url = newspaper_base_url + "category/tips/সেক্স-টিপস্/page/" + str(index)
        elif j == 30:
            url = newspaper_base_url + "category/tips/health-tips/page/" + str(index)
        elif j == 31:
            url = newspaper_base_url + "category/special/interview/page/" + str(index)
        elif j == 32:
            url = newspaper_base_url + "category/special/ঘোষনা/page/" + str(index)

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
                if len(link_tokens) == 5 and link_tokens[2] == "www.sasthabangla.com":
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
                    title = article_soup.find("title").get_text().split("-")[0].strip()
                except:
                    title = ""
                try:
                    article_content = article_soup.find("div", {"class": "entry-content"}).get_text().strip()
                except:
                    article_content = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
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
