import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import string

# 0 - 800
# 801 - 1600
# 1601 - 4060
lim1 = 800
lim2 = 1600
lim3 = 4060

newspaper_base_url = 'https://en.ittefaq.com.bd/'

stuck = 0
max_category = 8
max_national_pages = 4060
max_politics_pages = 729
max_international_pages = 2593
max_business_pages = 527
max_editorial_oped_pages = 94
max_sports_pages = 1761
max_sci_tech_pages = 1262
max_culture_pages = 1331
myLinks = ""
output_result = []
data = []
all_url = ""
prev_j = 0
for i in range(0, lim1):
    print(str(i + 1))
    with open("en_log.txt", 'a', encoding='utf8') as file:
        file.write(str(i + 1) + '\n')
    for j in range(max_category):
        if j == 0: url = newspaper_base_url + "national/page/" + str(i + 1)
        if j == 1:
            if max_politics_pages >= i + 1:
                url = newspaper_base_url + "politics/page/" + str(i + 1)
            else:
                url = "none"
        if j == 2:
            if max_international_pages >= i + 1:
                url = newspaper_base_url + "international/page/" + str(i + 1)
            else:
                url = "none"
        if j == 3:
            if max_business_pages >= i + 1:
                url = newspaper_base_url + "business/page/" + str(i + 1)
            else:
                url = "none"
        if j == 4:
            if max_editorial_oped_pages >= i + 1:
                url = newspaper_base_url + "editorial-oped/page/" + str(i + 1)
            else:
                url = "none"
        if j == 5:
            if max_sports_pages >= i + 1:
                url = newspaper_base_url + "sports/page/" + str(i + 1)
            else:
                url = "none"
        if j == 6:
            if max_sci_tech_pages >= i + 1:
                url = newspaper_base_url + "sci-tech/page/" + str(i + 1)
            else:
                url = "none"
        if j == 7:
            if max_culture_pages >= i + 1:
                url = newspaper_base_url + "culture/page/" + str(i + 1)
            else:
                url = "none"
        if not ("none" in url):
            print('\n' + url)

            archive_soup = ""
            try:
                archive_soup = requests.get(url, proxies={"http": proxy, "https": proxy})
            except:
                stuck = 1

            while stuck == 1:
                time.sleep(10)
                try:
                    archive_soup = requests.get(url)
                    stuck = 0
                except:
                    stuck = 1

            soup = BeautifulSoup(archive_soup.content, "html.parser")
            all_links = soup.find_all("a", attrs={"class": "read-more-link"})
            page_links_length = len(all_links)

            if page_links_length == 0:
                continue
            else:
                for link in all_links:
                    article_url = link.get('href')
                    article_data = ""
                    try:
                        article_data = requests.get(article_url)
                    except:
                        stuck = 1

                    while stuck == 1:
                        time.sleep(10)
                        try:
                            article_data = requests.get(article_url, proxies={"http": proxy, "https": proxy})
                            stuck = 0
                        except:
                            stuck = 1

                    article_soup = BeautifulSoup(article_data.content, "html.parser")

                    try:
                        article_title = article_soup.find("title")
                        article_title_text = str(article_title.text.strip())
                        article_title_text = article_title_text[0:len(article_title_text) - 16]
                    except:
                        article_title_text = ""
                    txtFiletitle = article_title_text
                    txtFiletitle = txtFiletitle.translate(str.maketrans('', '', string.punctuation))

                    try:
                        date_published = article_soup.find("time")['datetime']
                        date_published = date_published[0:10]
                    except:
                        date_published = "2000-01-01"
                    yr_mon_day = date_published.split('-')

                    print(article_url + " " + date_published)

                    url_parts = url.split('/')
                    output_dir = './{}/{}/{}/en'.format(yr_mon_day[0], yr_mon_day[1], yr_mon_day[2])
                    raw_output_dir = '../' + "Raw" + '/' + "Ittefaq.com" + '/' + output_dir
                    output_file_name = url_parts[3] + '_' + url_parts[4] + '_' + str(
                        i + 1) + '_' + txtFiletitle + "_abc.txt"
                    try:
                        os.makedirs(raw_output_dir)
                    except OSError:
                        pass
                    try:
                        with open(raw_output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                            file.write(str(article_soup))
                    except:
                        continue

                    paragraphs = article_soup.find_all("p")
                    textPart = ""
                    if len(paragraphs) > 0:
                        for para in paragraphs:
                            if len(para.attrs) == 0:
                                textPart += para.get_text() + "\n\n"
                    else:
                        textPart = ""

                    # article_content = article_soup.find_all("div", {"class": "content_detail"})
                    # article_body = article_soup.find("div", {"itemprop": "articleBody"})

                    data = "<article>\n"
                    data += "<title>" + article_title_text + "</title>\n"
                    data += "<date>" + date_published + "</date>\n"
                    data += "<text>\n" + textPart + "\n</text>\n"
                    data += "</article>"

                    try:
                        os.makedirs(output_dir)
                    except OSError:
                        pass
                    try:
                        with open(output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                            file.write(data + '\n')
                    except:
                        continue
                    # time.sleep(3)
