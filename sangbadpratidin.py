import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests


def month_converter(month):
    if month == "January":
        month = 1
    elif month == "February":
        month = 2
    elif month == "March":
        month = 3
    elif month == "April":
        month = 4
    elif month == "May":
        month = 5
    elif month == "June":
        month = 6
    elif month == "July":
        month = 7
    elif month == "August":
        month = 8
    elif month == "September":
        month = 9
    elif month == "October":
        month = 10
    elif month == "November":
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


newspaper_base_url = 'https://www.sangbadpratidin.in/'

for index in range(1, 300):
    for j in range(17):
        if j == 0:
            url = newspaper_base_url + "category/" + "coronavirus" + "/page/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "category/" + "kolkata" + "/page/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "category/" + "bengal" + "/page/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "category/" + "india" + "/page/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "category/" + "bangladesh" + "/page/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "category/" + "world" + "/page/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "category/" + "sports" + "/page/" + str(index)
        elif j == 7:
            url = newspaper_base_url + "category/" + "entertainment" + "/page/" + str(index)
        elif j == 8:
            url = newspaper_base_url + "category/" + "lifestyle" + "/page/" + str(index)
        elif j == 9:
            url = newspaper_base_url + "category/" + "offbeat" + "/page/" + str(index)
        elif j == 10:
            url = newspaper_base_url + "category/" + "science-and-environment" + "/page/" + str(index)
        elif j == 11:
            url = newspaper_base_url + "category/" + "editorial" + "/page/" + str(index)
        elif j == 12:
            url = newspaper_base_url + "category/" + "religion" + "/page/" + str(index)
        elif j == 13:
            url = newspaper_base_url + "category/" + "zodiac" + "/page/" + str(index)
        elif j == 14:
            url = newspaper_base_url + "category/" + "blog" + "/page/" + str(index)
        elif j == 15:
            url = newspaper_base_url + "category/" + "career" + "/page/" + str(index)
        elif j == 16:
            url = newspaper_base_url + "category/" + "farming" + "/page/" + str(index)

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
                if len(link_tokens) == 6 or len(link_tokens) == 7:
                    if link_tokens[2] == "www.sangbadpratidin.in":
                        article_url = link_separator
                    else:
                        continue
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
                    # date = article_soup.find("div",{"class":"date"}).get_text().split(",")[2].strip()
                    date = article_soup.find("p", {"class": "publish_date text-left mar-btm-20"})
                    date = date.find_all("span")
                    date = date[1].get_text().strip()
                    date_tokens = date.split(" ")

                    day = date_tokens[2].replace(",", "").strip()
                    month = month_converter(date_tokens[1])
                    year = date_tokens[3]
                except:
                    day = "01"
                    month = "01"
                    year = "2000"
                try:
                    title = article_soup.find_all("meta", {"property": "og:title"})[1].get('content')
                    title = title.strip()
                except:
                    title = ""
                try:
                    article_content = article_soup.find("div", {"class": "sp-single-post"}).get_text().strip()
                    author = article_content.split(":")[0]
                    article_content = " ".join(article_content.split(":")[1:])
                    article_content = article_content.replace("Highlights", "")
                    article_content = article_content.strip()
                    try:
                        author = author.split(",")[0].strip()
                    except:
                        pass
                    author = author.strip()

                except:
                    author = ""
                    article_content = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<author>" + author + "</author>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                if len(link_tokens) == 6:
                    output_file_name = link_tokens[4]
                elif len(link_tokens) == 7:
                    output_file_name = link_tokens[5]

                output_dir = './{}/{}/{}'.format(year, month, day)
                raw_output_dir = './' + "Raw/" + output_dir

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
