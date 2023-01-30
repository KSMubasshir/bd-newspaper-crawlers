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


newspaper_base_url = 'https://tutorialbd.com/'

for index in range(3, 16):
    for j in range(66):
        if j == 0:
            url = newspaper_base_url + "p/category/" + "featured-articles" + "/page/" + str(index)
        if j == 1:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/html-programming" + "/page/" + str(index)
        if j == 2:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/html5" + "/page/" + str(index)
        if j == 3:
            url = newspaper_base_url + "p/category/" + "ielts" + "/page/" + str(index)
        if j == 4:
            url = newspaper_base_url + "p/category/" + "auto-cad-2" + "/page/" + str(index)
        if j == 5:
            url = newspaper_base_url + "p/category/" + "online-marketing" + "/page/" + str(index)
        if j == 6:
            url = newspaper_base_url + "p/category/" + "uncategorized" + "/page/" + str(index)
        if j == 7:
            url = newspaper_base_url + "p/category/" + "ইমবেডেড-সিস্টেম/আরডুইনো" + "/page/" + str(index)
        if j == 9:
            url = newspaper_base_url + "p/category/" + "ইমবেডেড-সিস্টেম" + "/page/" + str(index)

        if j == 10:
            url = newspaper_base_url + "p/category/" + "illustrator" + "/page/" + str(index)
        if j == 11:
            url = newspaper_base_url + "p/category/" + "ইলেকট্রনিক্স-ক্লাসরুম" + "/page/" + str(index)
        if j == 12:
            url = newspaper_base_url + "p/category/" + "electronics" + "/page/" + str(index)
        if j == 13:
            url = newspaper_base_url + "p/category/" + "islam" + "/page/" + str(index)
        if j == 14:
            url = newspaper_base_url + "p/category/" + "এনিমেশন" + "/page/" + str(index)
        if j == 15:
            url = newspaper_base_url + "p/category/" + "android-2" + "/page/" + str(index)
        if j == 16:
            url = newspaper_base_url + "p/category/" + "ssc" + "/page/" + str(index)
        if j == 17:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/wordpress" + "/page/" + str(index)
        if j == 18:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/ওয়ার্ডপ্রেস-প্লাগিন" + "/page/" + str(index)
        if j == 19:
            url = newspaper_base_url + "p/category/" + "ওয়েব-এপ্লিকেশন" + "/page/" + str(index)

        if j == 20:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন" + "/page/" + str(index)
        if j == 21:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/web-hosting" + "/page/" + str(index)
        if j == 22:
            url = newspaper_base_url + "p/category/" + "c_hardware" + "/page/" + str(index)
        if j == 23:
            url = newspaper_base_url + "p/category/" + "math" + "/page/" + str(index)
        if j == 24:
            url = newspaper_base_url + "p/category/" + "graphics" + "/page/" + str(index)
        if j == 25:
            url = newspaper_base_url + "p/category/" + "notice" + "/page/" + str(index)
        if j == 26:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/javascript" + "/page/" + str(index)
        if j == 27:
            url = newspaper_base_url + "p/category/" + "life-style" + "/page/" + str(index)
        if j == 28:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/joomla-ওয়েব-ডিজাইন" + "/page/" + str(index)
        if j == 29:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/জে-কোয়েরী-jquery" + "/page/" + str(index)

        if j == 30:
            url = newspaper_base_url + "p/category/" + "ডাউনলোড" + "/page/" + str(index)
        if j == 31:
            url = newspaper_base_url + "p/category/" + "ইলেকট্রনিক্স-ক্লাসরুম/ডিজিটাল-ইলেকট্রনিক্স" + "/page/" + str(
                index)
        if j == 32:
            url = newspaper_base_url + "p/category/" + "ডেস্কটপ-এপ্লিকেশন" + "/page/" + str(index)
        if j == 33:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/drupal-2" + "/page/" + str(index)
        if j == 34:
            url = newspaper_base_url + "p/category/" + "3dstudiomax-এনিমেশন" + "/page/" + str(index)
        if j == 35:
            url = newspaper_base_url + "p/category/" + "network" + "/page/" + str(index)
        if j == 36:
            url = newspaper_base_url + "p/category/" + "education" + "/page/" + str(index)
        if j == 37:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/php" + "/page/" + str(index)
        if j == 38:
            url = newspaper_base_url + "p/category/" + "programming" + "/page/" + str(index)
        if j == 39:
            url = newspaper_base_url + "p/category/" + "c" + "/page/" + str(index)

        if j == 41:
            url = newspaper_base_url + "p/category/" + "প্রযুক্তি-পণ্য" + "/page/" + str(index)
        if j == 42:
            url = newspaper_base_url + "p/category/" + "প্রানী-জগত" + "/page/" + str(index)
        if j == 43:
            url = newspaper_base_url + "p/category/" + "photography" + "/page/" + str(index)
        if j == 44:
            url = newspaper_base_url + "p/category/" + "photoshop" + "/page/" + str(index)
        if j == 45:
            url = newspaper_base_url + "p/category/" + "professional" + "/page/" + str(index)
        if j == 46:
            url = newspaper_base_url + "p/category/" + "বই" + "/page/" + str(index)
        if j == 47:
            url = newspaper_base_url + "p/category/" + "sscbangla2" + "/page/" + str(index)
        if j == 48:
            url = newspaper_base_url + "p/category/" + "sscbangla" + "/page/" + str(index)
        if j == 49:
            url = newspaper_base_url + "p/category/" + "science" + "/page/" + str(index)

        if j == 50:
            url = newspaper_base_url + "p/category/" + "news" + "/page/" + str(index)
        if j == 51:
            url = newspaper_base_url + "p/category/" + "science/earth" + "/page/" + str(index)
        if j == 52:
            url = newspaper_base_url + "p/category/" + "science/research" + "/page/" + str(index)
        if j == 53:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/বুটস্ট্র্যাপ" + "/page/" + str(index)
        if j == 54:
            url = newspaper_base_url + "p/category/" + "blogging" + "/page/" + str(index)
        if j == 55:
            url = newspaper_base_url + "p/category/" + "future-technology" + "/page/" + str(index)
        if j == 56:
            url = newspaper_base_url + "p/category/" + "vb" + "/page/" + str(index)
        if j == 57:
            url = newspaper_base_url + "p/category/" + "flash" + "/page/" + str(index)
        if j == 58:
            url = newspaper_base_url + "p/category/" + "ইমবেডেড-সিস্টেম/মাইক্রোকন্ট্রোলার" + "/page/" + str(index)
        if j == 59:
            url = newspaper_base_url + "p/category/" + "মোবাইল-এপ্লিকেশন" + "/page/" + str(index)

        if j == 60:
            url = newspaper_base_url + "p/category/" + "লিনাক্স" + "/page/" + str(index)
        if j == 61:
            url = newspaper_base_url + "p/category/" + "aware" + "/page/" + str(index)
        if j == 62:
            url = newspaper_base_url + "p/category/" + "সফটওয়্যার" + "/page/" + str(index)
        if j == 63:
            url = newspaper_base_url + "p/category/" + "server" + "/page/" + str(index)
        if j == 64:
            url = newspaper_base_url + "p/category/" + "ওয়েব-ডিজাইন/css" + "/page/" + str(index)
        if j == 65:
            url = newspaper_base_url + "p/category/" + "health" + "/page/" + str(index)

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
                if len(link_tokens) == 6 and link_tokens[4].isnumeric():
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
                    title = article_soup.find("title").get_text().split("–")[0].strip()
                except:
                    title = ""
                try:
                    article_content = article_soup.find("div", {"class": "entry-content clear"}).get_text().strip()
                except:
                    article_content = ""
                try:
                    author = article_soup.find("span", {"class": "author-name"}).get_text().strip()
                except:
                    author = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<author>" + author + "</author>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[4]

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
