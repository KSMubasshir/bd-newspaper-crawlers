import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://www.jugantor.com/'
newspaper_archive_base_url = 'https://www.jugantor.com/archive/'

# start_date = date(2017, 10, 12)
# end_date = date(2018, 9, 11)
start_date = date(2017, 12, 18)
end_date = date.today()
delta = end_date - start_date
output_result = []
data = []
exceptions = 0

for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    print(date_str)
    index = 0
    output_dir = './{}/{}/{}/bn'.format(date_str.year, date_str.month, date_str.day)
    raw_output_dir = '../' + "Raw" + '/' + "Jugantor" + '/' + output_dir
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass

    index = index + 1
    url = newspaper_archive_base_url + str(date_str.year) + "/" + str(date_str.month) + "/" + str(date_str.day)
    try:
        archive_soup = requests.get(url)
    except:
        print("No response for links in archive,trying to reconnect")
        time.sleep(2)
        continue
    print(url)
    soup = BeautifulSoup(archive_soup.content, "html.parser")

    all_links = soup.find_all("a")
    page_links_length = len(all_links)

    if page_links_length == 0:
        break
    else:
        for link in all_links:
            article_url = link.get('href')
            link_separator = article_url.split('/')
            if len(link_separator) != 6 or link_separator[2] != "www.jugantor.com":
                continue
            if link_separator[3] == "covid-19":
                output_file_name = '{}_{}.txt'.format(link_separator[3], link_separator[4])
                title = ""
            else:
                output_file_name = '{}_{}_{}.txt'.format(link_separator[3], link_separator[4], link_separator[5])
                title = link_separator[5]
                title = title.replace("-", " ")
            print(article_url)
            try:
                article_data = requests.get(article_url).text
            except:
                print("No response for content in link,trying to reconnect")
                time.sleep(2)
                continue
            with open(raw_output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
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

                elif i <= length - 5:
                    article_content += paragraph.get_text() + "\n"
                else:
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
