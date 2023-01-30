import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://samakal.com/'
newspaper_archive_base_url = 'https://samakal.com/archive/'  # ?date=2014-01-01&page=0

start_date = date(2014, 1, 1)
end_date = date.today()
delta = end_date - start_date
output_result = []
data = []
exceptions = 0

for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    print(date_str)
    output_dir = './{}/{}/{}/bn'.format(date_str.year, date_str.month, date_str.day)
    raw_output_dir = '../' + "Raw" + '/' + "Samakal" + '/' + output_dir
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass
    for index in range(15):
        url = newspaper_archive_base_url + '?date=' + str(date_str) + '&page=' + str(index)
        try:
            print(url)
            archive_soup = requests.get(url)
        except:
            print("No response for links in archive,trying to reconnect")
            time.sleep(2)
            continue
        soup = BeautifulSoup(archive_soup.content, "html.parser")
        all_links = soup.find_all("a", attrs={"class": "link-overlay"})
        page_links_length = len(all_links)

        if page_links_length == 0:
            break
        else:
            for link in all_links:
                article_url = link.get('href')
                link_separator = link.get('href').split('/')
                output_file_name = '{}_{}_{}_{}.txt'.format(link_separator[3], link_separator[4], link_separator[5],
                                                            link_separator[6])
                title = link_separator[6]
                title = title.replace("-", " ")
                try:
                    print(article_url)
                    article_data = requests.get(article_url).text
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue
                with open(raw_output_dir + '/' + output_file_name, 'w') as file:
                    file.write(str(article_url) + '\n' + str(article_data))

                article_soup = BeautifulSoup(article_data, "html.parser")

            paragraphs = article_soup.find_all("p")

            # title = article_soup.find("h1").get_text()

            length = len(paragraphs)
            length = length - 1

            i = 0

            article_content = ""
            for paragraph in paragraphs:
                if i == 0:
                    Author_date = paragraph.get_text().splitlines()
                    author = Author_date[0]
                    date = Author_date[1]
                    date = date.split(",")[0]
                    article_content += paragraph.get_text() + "\n"


                elif i <= length - 5:
                    article_content += paragraph.get_text() + "\n"
                else:
                    article_content += paragraph.get_text() + "\n"

                    pass
                i = i + 1

            data = "<article>\n"
            data += "<title>" + title + "</title>\n"
            data += "<date>" + date + "</date>\n"
            data += "<author>" + author + "</author>\n"
            data += "<text>\n" + article_content + "</text>\n"
            data += "</article>"

            with open(output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                file.write(data + '\n\n')
