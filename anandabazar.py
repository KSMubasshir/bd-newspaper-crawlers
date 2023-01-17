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
    elif month == "অগস্ট":
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


newspaper_base_url = 'https://www.anandabazar.com/'

for index in range(1, 300):
    for j in range(6):
        if j == 0:
            url = newspaper_base_url + "state" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 1:
            url = newspaper_base_url + "district/howrah-hoogly" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 2:
            url = newspaper_base_url + "district/north-bengal" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 3:
            url = newspaper_base_url + "district/24-paraganas" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 4:
            url = newspaper_base_url + "district/nadia-murshidabad" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 5:
            url = newspaper_base_url + "district/purulia-birbhum-bankura" + "/archive?page=" + str(
                index) + "&slab=0&tnp=50"
        elif j == 6:
            url = newspaper_base_url + "district/bardhaman" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 7:
            url = newspaper_base_url + "district/midnapore" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 8:
            url = newspaper_base_url + "international" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 9:
            url = newspaper_base_url + "business" + "/archive?page=" + str(index) + "&slab=0&tnp=50"

        elif j == 10:
            url = newspaper_base_url + "editorial" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 11:
            url = newspaper_base_url + "sport" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 12:
            url = newspaper_base_url + "entertainment" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 13:
            url = newspaper_base_url + "lifestyle" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 14:
            url = newspaper_base_url + "travel" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 15:
            url = newspaper_base_url + "editorial" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 16:
            url = newspaper_base_url + "sport" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 17:
            url = newspaper_base_url + "entertainment" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 18:
            url = newspaper_base_url + "lifestyle" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 19:
            url = newspaper_base_url + "travel" + "/archive?page=" + str(index) + "&slab=0&tnp=50"

        elif j == 20:
            url = newspaper_base_url + "horoscope/articles?page=" + str(index)
        elif j == 21:
            url = newspaper_base_url + "supplementary/rabibashoriyo" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 22:
            url = newspaper_base_url + "supplementary/patrika" + "/archive?page=" + str(index) + "&slab=0&tnp=50"
        elif j == 23:
            url = newspaper_base_url + "supplementary/kolkatakorcha" + "/archive?page=" + str(index) + "&slab=0&tnp=7"
        elif j == 24:
            url = newspaper_base_url + "supplementary/pustokporichoi" + "/archive?page=" + str(index) + "&slab=0&tnp=50"

        try:
            print(url)
            archive_soup = requests.get(url)
        except:
            print("No response for links in archive,passing")
            continue

        soup = BeautifulSoup(archive_soup.content, "html.parser")

        all_links = soup.find_all("a", {"class": "thumbnail"})
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
                if len(link_tokens) == 3:
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
                    # date = article_soup.find("div",{"class":"date"}).get_text().split(",")[2].strip()
                    date = article_soup.find_all("li", {"class": "publish-date"})[1].get_text().strip()
                    date_tokens = date.split(",")

                    day_month = date_tokens[0]

                    day = day_month.split(" ")[0].strip()
                    month = day_month.split(" ")[1].strip()
                    year = date_tokens[1].strip()

                    date = day + " " + month + ", " + year

                    day = date_translator(day)
                    month = month_converter(month)
                    year = date_translator(year)

                except:
                    date = "০১/০১/২০০০"
                    day = "01"
                    month = "01"
                    year = "2000"
                try:
                    title = article_soup.find("meta", {"property": "og:title"}).get('content').strip()
                except Exception as e:
                    print(str(e))
                    title = ""
                try:
                    article_content = article_soup.find_all("body")
                    article_content = article_content[1].get_text().strip()
                except:
                    article_content = ""
                try:
                    author = article_soup.find("meta", {"name": "author"}).get('content').strip()
                except:
                    author = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<date>" + date + "</date>\n"
                data += "<author>" + author + "</author>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[2]

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
