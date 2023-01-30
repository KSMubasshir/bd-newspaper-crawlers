import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://bengali.indianexpress.com/'

for index in range(1, 300):
    for j in range(9):
        if j == 0:
            url = newspaper_base_url + "general-news" + "/page/" + str(index)
        if j == 1:
            url = newspaper_base_url + "politics" + "/page/" + str(index)
        if j == 2:
            url = newspaper_base_url + "world" + "/page/" + str(index)
        if j == 3:
            url = newspaper_base_url + "entertainment" + "/page/" + str(index)
        if j == 4:
            url = newspaper_base_url + "lifestyle" + "/page/" + str(index)
        if j == 5:
            url = newspaper_base_url + "opinion" + "/page/" + str(index)
        if j == 6:
            url = newspaper_base_url + "technology" + "/page/" + str(index)
        if j == 7:
            url = newspaper_base_url + "explained" + "/page/" + str(index)
        if j == 8:
            url = newspaper_base_url + "sports" + "/page/" + str(index)

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
                if len(link_tokens) == 6:
                    if link_tokens[2] == "bengali.indianexpress.com":
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
                    title = article_soup.find("title").get_text().split("–")[0].strip()
                except:
                    title = ""
                try:
                    article_content = article_soup.find("h2").get_text().strip()
                    article_content += article_soup.find("div", {"class": "full-details"}).get_text().strip()
                    article_content = article_content.replace("Read in English", "")
                    article_content = article_content.replace("Read the story in English", "")
                    article_content = article_content.replace("Read the full story in English", "")
                    article_content = article_content.replace(
                        "Get all the Latest Bengali News and West Bengal News at Indian Express Bangla. You can also "
                        "catch all the General  News in Bangla by following us on Twitter and Facebook",
                        "")
                except:
                    article_content += ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                output_file_name = link_tokens[4]

                output_dir = "./Data/"
                raw_output_dir = './' + "Raw/"

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
