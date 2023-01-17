import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

# from io import open

newspaper_base_url = 'http://biggani.org/'

output_result = []
data = []
exceptions = 0

for index in range(1, 100):
    for j in range(40):
        if j == 0:
            url = newspaper_base_url + "?cat=25&paged=" + str(index)
        elif j == 1:
            url = newspaper_base_url + "?cat=893&paged=" + str(index)
        elif j == 2:
            url = newspaper_base_url + "?cat=28&paged=" + str(index)
        elif j == 3:
            url = newspaper_base_url + "?cat=30&paged=" + str(index)
        elif j == 4:
            url = newspaper_base_url + "?cat=32&paged=" + str(index)
        elif j == 5:
            url = newspaper_base_url + "?cat=44&paged=" + str(index)
        elif j == 6:
            url = newspaper_base_url + "?cat=47&paged=" + str(index)
        elif j == 7:
            url = newspaper_base_url + "?cat=24&paged=" + str(index)
        elif j == 8:
            url = newspaper_base_url + "?cat=17&paged=" + str(index)
        elif j == 9:
            url = newspaper_base_url + "?cat=866&paged=" + str(index)
        elif j == 10:
            url = newspaper_base_url + "?cat=35&paged=" + str(index)
        elif j == 11:
            url = newspaper_base_url + "?cat=27&paged=" + str(index)
        elif j == 12:
            url = newspaper_base_url + "?cat=914&paged=" + str(index)
        elif j == 13:
            url = newspaper_base_url + "?cat=14&paged=" + str(index)
        elif j == 14:
            url = newspaper_base_url + "?cat=19&paged=" + str(index)
        elif j == 15:
            url = newspaper_base_url + "?cat=37&paged=" + str(index)
        elif j == 16:
            url = newspaper_base_url + "?cat=43&paged=" + str(index)
        elif j == 18:
            url = newspaper_base_url + "?cat=16&paged=" + str(index)
        elif j == 19:
            url = newspaper_base_url + "?cat=15&paged=" + str(index)
        elif j == 20:
            url = newspaper_base_url + "?cat=21&paged=" + str(index)
        elif j == 21:
            url = newspaper_base_url + "?cat=864&paged=" + str(index)
        elif j == 22:
            url = newspaper_base_url + "?cat=865&paged=" + str(index)
        elif j == 23:
            url = newspaper_base_url + "?cat=33&paged=" + str(index)
        elif j == 24:
            url = newspaper_base_url + "?cat=18&paged=" + str(index)
        elif j == 25:
            url = newspaper_base_url + "?cat=911&paged=" + str(index)
        elif j == 26:
            url = newspaper_base_url + "?cat=12&paged=" + str(index)
        elif j == 27:
            url = newspaper_base_url + "?cat=26&paged=" + str(index)
        elif j == 28:
            url = newspaper_base_url + "?cat=22&paged=" + str(index)
        elif j == 29:
            url = newspaper_base_url + "?cat=31&paged=" + str(index)
        elif j == 30:
            url = newspaper_base_url + "?cat=36&paged=" + str(index)
        elif j == 31:
            url = newspaper_base_url + "?cat=20&paged=" + str(index)
        elif j == 32:
            url = newspaper_base_url + "?cat=3&paged=" + str(index)
        elif j == 33:
            url = newspaper_base_url + "?cat=159&paged=" + str(index)
        elif j == 34:
            url = newspaper_base_url + "?cat=13&paged=" + str(index)
        elif j == 35:
            url = newspaper_base_url + "?cat=34&paged=" + str(index)
        elif j == 36:
            url = newspaper_base_url + "?cat=23&paged=" + str(index)
        elif j == 37:
            url = newspaper_base_url + "?cat=39&paged=" + str(index)
        elif j == 38:
            url = newspaper_base_url + "?cat=912&paged=" + str(index)
        elif j == 39:
            url = newspaper_base_url + "?cat=48&paged=" + str(index)
        print(url)

        try:
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
                if len(link_tokens) == 4:
                    if "?p=" in link_tokens[3]:
                        if "respond" in link_tokens[3] or "comments" in link_tokens[3]:
                            continue
                        else:
                            article_url = link_separator
                    else:
                        continue
                else:
                    continue

                output_file_name = link_tokens[3][3:]

                output_dir = "./Data"
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
                    print(article_url)
                    article_data = requests.get(article_url).text
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue
                article_soup = BeautifulSoup(article_data, "html.parser")
                with open(raw_output_dir + '/' + output_file_name, 'w') as file:
                    file.write(str(article_soup))

                try:
                    article_content = article_soup.find("div", {"class": "entry"}).get_text(separator='\n')
                except:
                    article_content = ""

                try:
                    author = article_soup.find("span", {"class": "post-meta-author"}).get_text().strip()
                except:
                    author = ""

                try:
                    title = article_soup.find("title").get_text().split("-")[0].strip()
                except:
                    title = ""

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<author>" + author + "</author>\n"
                data += "<text>\n" + article_content + "\n</text>\n"
                data += "</article>"

                try:
                    with open(output_dir + '/' + output_file_name, 'w') as file:
                        file.write(data.encode('utf-8'))
                except:
                    pass
