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


newspaper_base_url = 'https://eisamay.indiatimes.com/'

for index in range(0, 3300):
    for j in range(37):
        if j == 0:
            url = newspaper_base_url + "west-bengal-news/kolkata-news/articlelist/15991773.cms?curpg=" + str(index)
        if j == 1:
            url = newspaper_base_url + "west-bengal-news/hooghly-news/articlelist/49780499.cms?curpg=" + str(index)
        if j == 2:
            url = newspaper_base_url + "west-bengal-news/howrah-news/articlelist/15991767.cms?curpg=" + str(index)
        if j == 3:
            url = newspaper_base_url + "west-bengal-news/24pargana-news/articlelist/49780592.cms?curpg=" + str(index)
        if j == 4:
            url = newspaper_base_url + "west-bengal-news/bardhaman-news/articlelist/51647343.cms?curpg=" + str(index)
        if j == 5:
            url = newspaper_base_url + "west-bengal-news/durgapur-news/articlelist/51683233.cms?curpg=" + str(index)
        if j == 6:
            url = newspaper_base_url + "west-bengal-news/asansol-news/articlelist/51683248.cms?curpg=" + str(index)
        if j == 7:
            url = newspaper_base_url + "west-bengal-news/others/articlelist/64076363.cms?curpg=" + str(index)
        if j == 8:
            url = newspaper_base_url + "nation/articlelist/15819599.cms?curpg=" + str(index)
        if j == 9:
            url = newspaper_base_url + "world/articlelist/15819594.cms?curpg=" + str(index)

        if j == 10:
            url = newspaper_base_url + "bangladesh-news/articlelist/62281110.cms?curpg=" + str(index)
        if j == 11:
            url = newspaper_base_url + "sports/other-sports/articlelist/15819612.cms?curpg=" + str(index)
        if j == 12:
            url = newspaper_base_url + "sports/cricket/news/articlelist/16570436.cms?curpg=" + str(index)
        if j == 13:
            url = newspaper_base_url + "sports/football/news/articlelist/15819590.cms?curpg=" + str(index)
        if j == 14:
            url = newspaper_base_url + "education-news/articlelist/76781032.cms?curpg=" + str(index)
        if j == 15:
            url = newspaper_base_url + "business/business-news/articlelist/15819574.cms?curpg=" + str(index)
        if j == 16:
            url = newspaper_base_url + "lifestyle/health-fitness/articlelist/15992584.cms?curpg=" + str(index)
        if j == 17:
            url = newspaper_base_url + "lifestyle/relationship/articlelist/68252641.cms?curpg=" + str(index)
        if j == 18:
            url = newspaper_base_url + "/lifestyle/food/articlelist/15992590.cms?curpg=" + str(index)
        if j == 19:
            url = newspaper_base_url + "entertainment/film-review/articlelist/15900258.cms?curpg=" + str(index)

        if j == 20:
            url = newspaper_base_url + "lifestyle/work-life/articlelist/15992570.cms?curpg=" + str(index)
        if j == 21:
            url = newspaper_base_url + "lifestyle/news-on-travel/articlelist/47865219.cms?curpg=" + str(index)
        if j == 22:
            url = newspaper_base_url + "lifestyle/home-and-family/articlelist/20586149.cms?curpg=" + str(index)
        if j == 23:
            url = newspaper_base_url + "lifestyle/bookcase/articlelist/35619160.cms?curpg=" + str(index)
        if j == 24:
            url = newspaper_base_url + "lifestyle/section-for-kids/articlelist/21052348.cms?curpg=" + str(index)
        if j == 25:
            url = newspaper_base_url + "lifestyle/live-your-dreams/articlelist/20890497.cms?curpg=" + str(index)
        if j == 26:
            url = newspaper_base_url + "tech/news/articlelist/15992443.cms?curpg=" + str(index)
        if j == 27:
            url = newspaper_base_url + "tech/mobile-review/articlelist/64760842.cms?curpg=" + str(index)
        if j == 28:
            url = newspaper_base_url + "tech/how-to/articlelist/64760860.cms?curpg=" + str(index)
        if j == 29:
            url = newspaper_base_url + "viral-news-truth/articlelist/64352062.cms?curpg=" + str(index)

        if j == 30:
            url = newspaper_base_url + "crime/articlelist/68271919.cms?curpg=" + str(index)
        if j == 31:
            url = newspaper_base_url + "auto-news/articlelist/63397979.cms?curpg=" + str(index)
        if j == 32:
            url = newspaper_base_url + "editorial/interviews/articlelist/15992010.cms?curpg=" + str(index)
        if j == 33:
            url = newspaper_base_url + "editorial/edit/articlelist/15992022.cms?curpg=" + str(index)
        if j == 34:
            url = newspaper_base_url + "editorial/post-editorial/articlelist/21272752.cms?curpg=5" + str(index)
        if j == 35:
            url = newspaper_base_url + "citizen-reporter/citizenreporter.cms?curpg=" + str(index)
        if j == 36:
            url = "https://blogs.eisamay.indiatimes.com/page/" + str(index)

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

                if len(link_tokens) < 7:
                    continue

                if link_tokens[2] == "eisamay.indiatimes.com":
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
                    title = article_soup.find("h1", {"itemprop": "headline"}).get_text()
                except:
                    title = ""
                try:
                    article_content = ""
                    article_contents = article_soup.find("article", {"itemprop": "articleBody"}).get_text().split(":")

                    i = 0
                    for splits in article_contents:
                        if i == 0:
                            i += 1
                        else:
                            article_content += splits
                            i += 1
                    article_content = article_content.strip()

                except:
                    try:
                        article_contents = article_soup.find("article", {"itemprop": "articleBody"}).get_text()
                    except:
                        article_content = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[len(link_tokens) - 1]

                output_dir = './Data/'
                raw_output_dir = './' + "Raw" + '/'

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
