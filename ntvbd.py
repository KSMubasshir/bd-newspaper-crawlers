import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'https://www.ntvbd.com'
newspaper_archive_base_url = 'https://www.ntvbd.com/archive/'

start_date = date(2015, 1, 28)
end_date = date.today()
delta = end_date - start_date
output_result = []
data = []
exceptions = 0

for i in range(delta.days + 1):
    date_str = start_date + timedelta(days=i)
    print(date_str)
    index = 0
    output_dir = './{}/{}/{}/bn'.format(date_str.year, date_str.month,date_str.day)
    raw_output_dir = '../'+ "Raw" + '/' + "ntvbd" + '/' + output_dir
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
        archive_soup =  requests.get(url)
    except:
        print("No response for links in archive,trying to reconnect")
        time.sleep(2)
        continue
    print(url)
    soup = BeautifulSoup(archive_soup.content, "html.parser")

    all_links = soup.find_all("a")
    page_links_length = len(all_links)

    if(page_links_length == 0):
        break
    else:
        for link in all_links:
            try :
                article_url = link.get('href')
                link_separator = article_url.split('/')
            except :
                continue
            if len(link_separator) != 4 :
                continue 
            if link_separator[2].isnumeric() == False :
                continue
            
            output_file_name = link_separator[1] + "_" + link_separator[2]
            article_url = newspaper_base_url + article_url
            print(article_url)

            try:
                article_data = requests.get(article_url).text
            except:
                print("No response for content in link,trying to reconnect")
                time.sleep(2)
                continue

            with open(raw_output_dir + '/' + output_file_name, 'w') as file:
                file.write(article_data.encode('utf-8'))
            
            article_soup = BeautifulSoup(article_data, "html.parser")

            paragraphs = article_soup.find_all("p")

            title = article_soup.find("meta",{"property":"og:title"}).get('content')
            try:
                author =  article_soup.find("strong",{"class":"color-black"}).get_text()
            except:
                author = ""

            try:
                date =  article_soup.find("div",{"class":"date color-gray"}).get_text()
            except:
                date = ""

            length = len(paragraphs)
            length = length - 1

            i = 0

            article_content = ""
            for paragraph in paragraphs: 
                if i <= length - 5 :
                    article_content += paragraph.get_text() + "\n"
                else :
                    pass
                i = i + 1
            
            

            data  =  "<article>\n"
            data +=  "<title>"       + title            + "</title>\n"
            data +=  "<date>"        + date             + "</date>\n"
            data +=  "<author>"      + author           + "</author>\n"
            data +=  "<text>\n"      + article_content  + "</text>\n"
            data +=  "</article>"

            with open(output_dir+ '/' + output_file_name, 'w') as file:
                file.write(data.encode('utf-8'))