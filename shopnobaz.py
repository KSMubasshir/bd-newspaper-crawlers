import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

base_url = 'http://shopnobaz.net/page/'

for index in range(400, 1000):
    url = base_url + str(index)
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
            if len(link_tokens) == 6:
                if "respond" in link_tokens[5] or "comments" in link_tokens[5]:
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
                title = article_soup.find("h1").get_text()
            except:
                title = ""
            try:
                article_content = article_soup.find("div", {"class": "entry-content clearfix"}).get_text()
            except:
                article_content = ""

            data = "<article>\n"
            data += "<title>" + title + "</title>\n"
            data += "<text>\n" + article_content + "\n</text>\n"
            data += "</article>"

            output_file_name = link_tokens[5]
            output_dir = "./ShonoBaz/"
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
