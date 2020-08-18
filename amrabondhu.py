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
   
newspaper_base_url = 'https://www.amrabondhu.com'

for index in range( 421 ):
        url = newspaper_base_url + "/node?page=" + str(index)
        try:
            print(url)
            archive_soup =  requests.get(url)
        except:
            print("No response for links in archive,passing")
            continue
        soup = BeautifulSoup(archive_soup.content, "html.parser")

        all_links = soup.find_all("a")
        page_links_length = len(all_links)

        if(page_links_length == 0):
            break
        else:
            for link in all_links:
                link_separator = link.get('href')
                
                try:
                    link_tokens = link_separator.split("/")
                except:
                    continue
                if len( link_tokens) == 3 and link_tokens[2].isnumeric():
                    article_url = newspaper_base_url + link_separator
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
                    date = article_soup.find("div",{"class":"art-PostHeaderIcons art-metadata-icons"}).get_text().strip()
                    date = date.split("|")[1].split("-")[0].strip()
                except:
                    date = "০১/০১/২০০০"
                try:
                    title = article_soup.find("title").get_text().split("|")[0].strip()
                except:
                    title=""
                try:
                    article_content = article_soup.find("div",{"class":"art-article"}).get_text().strip()
                except:
                    article_content = ""
                try:
                    author = article_soup.find("a",{"title":"View user profile."}).get_text().strip()
                except:
                    author = ""

                data  =  "<article>\n"
                data +=  "<title>" + title + "</title>\n"     
                data +=  "<date>" + date + "</date>\n"     
                data +=  "<author>" + author + "</author>\n"     
                data +=  "<text>\n" + article_content + "\n</text>\n"
                data +=  "</article>"

                

                output_file_name = link_tokens[1] + "_" + link_tokens[2]

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
                    with open(raw_output_dir+ '/' + output_file_name, 'w', encoding = 'utf8') as file:
                        file.write(str(article_soup))
                except:
                    pass

                try:
                    with open(output_dir+ '/' + output_file_name, 'w', encoding = 'utf8') as file:
                        file.write(data)
                except:
                    pass