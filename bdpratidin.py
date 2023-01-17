import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

# from io import open

newspaper_base_url = 'https://www.bd-pratidin.com/'

output_result = []
data = []
exceptions = 0

for i in range(100):
    index = i * 12

    for j in range(28):
        if j == 0:
            url = newspaper_base_url + "national/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "city-news/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "country/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "international-news/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "entertainment/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "sports/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "mixter/" + str(index)
        elif j == 7:
            url = newspaper_base_url + "chayer-desh/" + str(index)
        elif j == 8:
            url = newspaper_base_url + "probash-potro/" + str(index)
        elif j == 9:
            url = newspaper_base_url + "campus-online/" + str(index)
        elif j == 10:
            url = newspaper_base_url + "facebook/" + str(index)
        elif j == 11:
            url = newspaper_base_url + "islam/" + str(index)
        elif j == 12:
            url = newspaper_base_url + "minister-spake/" + str(index)
        elif j == 13:
            url = newspaper_base_url + "corporate-corner/" + str(index)
        elif j == 14:
            url = newspaper_base_url + "chittagong-pratidin/" + str(index)
        elif j == 15:
            url = newspaper_base_url + "coronavirus/" + str(index)
        elif j == 16:
            url = newspaper_base_url + "Coronal-literature/" + str(index)
        elif j == 18:
            url = newspaper_base_url + "open-air-theater/" + str(index)
        elif j == 19:
            url = newspaper_base_url + "life/" + str(index)
        elif j == 20:
            url = newspaper_base_url + "health-tips/" + str(index)
        elif j == 21:
            url = newspaper_base_url + "city-roundup/" + str(index)
        elif j == 22:
            url = newspaper_base_url + "features/" + str(index)
        elif j == 23:
            url = newspaper_base_url + "job-market/" + str(index)
        elif j == 24:
            url = newspaper_base_url + "readers-column/" + str(index)
        elif j == 25:
            url = newspaper_base_url + "abroad-paper/" + str(index)
        elif j == 26:
            url = newspaper_base_url + "kolkata/" + str(index)
        elif j == 27:
            url = newspaper_base_url + "tech-world/" + str(index)

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
                link_tokens = link_separator.split("/")
                if len(link_tokens) == 5:
                    link = "https://www.bd-pratidin.com/" + link_separator
                else:
                    continue
                article_url = link

                year = link_tokens[1]
                month = link_tokens[2]
                day = link_tokens[3]

                if year.startswith('20'):
                    print(article_url)
                else:
                    continue

                output_file_name = link_tokens[0] + "_" + link_tokens[1] + "_" + link_tokens[2] + "_" + link_tokens[
                    3] + "_" + link_tokens[4]

                output_dir = './{}/{}/{}/bn'.format(year, month, day)
                raw_output_dir = '../' + "Raw" + '/' + "BangladeshPratidin" + '/' + output_dir

                try:
                    os.makedirs(output_dir)
                except OSError:
                    pass
                try:
                    os.makedirs(raw_output_dir)
                except OSError:
                    pass

                try:
                    article_data = requests.get(article_url).text
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue
                article_soup = BeautifulSoup(article_data, "html.parser")
                with open(raw_output_dir + '/' + output_file_name, 'w') as file:
                    file.write(str(article_soup))

                print(article_url)
                paragraphs = article_soup.find_all("p")

                title = article_soup.find("h1").get_text()

                length = len(paragraphs)
                length = length - 1

                i = 0

                article_content = ""
                for paragraph in paragraphs:
                    if i == 0:
                        date = str(i) + " " + paragraph.get_text()
                    elif i != length:
                        article_content += str(i) + " " + paragraph.get_text() + "\n"
                    else:
                        pass
                    i = i + 1

                data = "<article>\n"
                data += "<title>" + title + "</title>\n"
                data += "<date>" + date + "</date>\n"
                data += "<text>" + article_content + "</text>\n"
                data += "</article>"

                try:
                    with open(output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                        file.write(data)
                except:
                    pass
