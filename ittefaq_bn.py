import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://www.ittefaq.com.bd/'
newspaper_archive_base_url = 'https://www.ittefaq.com.bd/archives/'

# start_date = date(2019,  4, 30)
# end_date   = date.today()
start_date = date(2019, 4, 30)
end_date = date.today()
delta = end_date - start_date
output_result = []
data = []

for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)

    month = str(date_str.month)
    day = str(date_str.day)
    if date_str.month < 10: month = "0" + month
    if date_str.day < 10:   day = "0" + day

    output_dir = './{}/{}/{}/bn'.format(date_str.year, date_str.month, date_str.day)
    raw_output_dir = '../' + "Raw" + '/' + "Ittefaq.com" + '/' + output_dir

    try:
        os.makedirs(output_dir)
    except OSError:
        pass

    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass

    url = newspaper_archive_base_url + 'online-edition/{}/{}/{}'.format(date_str.year, month, day)
    print(date_str)
    print("online-edition")

    # url = newspaper_archive_base_url + 'print-edition/{}/{}/{}'.format(date_str.year, month , day)
    # print(date_str)
    # print("print-edition")
    with open("bn_log.txt", 'a', encoding='utf8') as file:
        file.write(str(date_str) + ' ' + "online-edition" + '\n')

    try:
        archive_soup = requests.get(url)
    except:
        print("No response for links in archive,trying to reconnect")
        time.sleep(2)
        continue

    soup = BeautifulSoup(archive_soup.content, "html.parser")
    # with open("debug.txt", 'w', encoding='utf8') as file:
    # file.write(str(soup))
    # exit()
    all_links = soup.find_all("a", attrs={"class": ""})
    page_links_length = len(all_links)

    if page_links_length == 0:
        break
    else:
        for link in all_links:
            article_url = link.get('href')

            link_separator = link.get('href').split('/')
            link_separator_len = len(link_separator)

            if link_separator_len == 6:
                if "79445" in link_separator[4]: continue
                if "79444" in link_separator[4]: continue
                if "79443" in link_separator[4]: continue
                if "79442" in link_separator[4]: continue
                if "79441" in link_separator[4]: continue
                if "79440" in link_separator[4]: continue
                if "79386" in link_separator[4]: continue
                if "79388" in link_separator[4]: continue
                if "79397" in link_separator[4]: continue
                if "79402" in link_separator[4]: continue
                if "79420" in link_separator[4]: continue
                if "79421" in link_separator[4]: continue
                if "79428" in link_separator[4]: continue
                if "79418" in link_separator[4]: continue
                if "79414" in link_separator[4]: continue
                if "79411" in link_separator[4]: continue
                print(article_url)
                output_file_name = 'bn_{}_{}.txt'.format(link_separator[3], link_separator[4])

                try:
                    article_data = requests.get(article_url)
                except:
                    print("No response,trying to reconnect")
                    time.sleep(2)
                    continue
                article_soup = BeautifulSoup(article_data.content, "html.parser")

                with open(raw_output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                    file.write(str(article_url) + '\n' + str(article_soup))

                try:
                    article_title = article_soup.find("div", {"class": "dtl_hl_block"})
                    article_title_text = str(article_title.text.strip())
                except:
                    article_title_text = ""

                tags = ""
                try:
                    tag_list = article_soup.find("div", {"id": "tags_list"})
                    tags = tag_list.get_text()
                except:
                    tags = ""

                try:
                    article_body = article_soup.find("div", {"class": "dtl_content_block"})
                    article_body_text = article_body.get_text(separator="\n\n")
                except:
                    article_body_text = ""

                data = "<article>\n"
                data += "<title>" + article_title_text + "</title>\n"
                data += "<date>" + str(date_str) + "</date>\n"
                data += "<topic>" + tags + "</topic>\n"
                data += "<text>\n" + article_body_text + "\n</text>\n"
                data += "</article>"

                with open(output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                    file.write(data + '\n')
        exit()
