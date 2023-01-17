import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'http://banglablog.in/sitemap/'

try:
    print(newspaper_base_url)
    archive_soup = requests.get(newspaper_base_url)
except:
    print("No response for links in archive,passing")
    pass

soup = BeautifulSoup(archive_soup.content, "html.parser")

all_links = soup.find_all("a")
page_links_length = len(all_links)

if (page_links_length == 0):
    exit()
else:
    for link in all_links:
        link_separator = link.get('href')

        try:
            link_tokens = link_separator.split("/")
        except:
            pass
        if len(link_tokens) == 6:
            article_url = link_separator
        else:
            continue

        try:
            print(article_url)
            article_data = requests.get(article_url).text
        except:
            print("No response for content in link,trying to reconnect")
            time.sleep(2)
            pass

        article_soup = BeautifulSoup(article_data, "html.parser")

        try:
            paragraphs = article_soup.find_all("p")
        except:
            continue

        try:
            title = article_soup.find("title").get_text().split("-")[0].strip()
        except:
            title = ""

        try:
            author = article_soup.find("span", {"rel": "author"}).get_text()
        except:
            author = ""

        article_content = ""
        i = 0
        length = len(paragraphs)
        for paragraph in paragraphs:
            if i <= 3:
                pass
            elif i > length - 28:
                pass
            else:
                article_content += paragraph.get_text()
            i = i + 1

        data = "<article>\n"
        data += "<title>" + title + "</title>\n"
        data += "<text>\n" + article_content + "\n</text>\n"
        data += "</article>"

        output_file_name = link_tokens[4]
        output_dir = "./Banglablog/"
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
