import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests

newspaper_base_url = 'http://www.prothom-alo.com/'
newspaper_archive_base_url = 'http://www.prothom-alo.com/archive/'

#start_date = date(2017, 10, 12)
#end_date = date(2018, 9, 11)
start_date = date(2018, 9, 12)
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
    raw_output_dir = '../'+ "Raw" + '/' + "Prothom_Alo.com" + '/' + output_dir
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass

    while(True):
        index = index + 1
        url = newspaper_archive_base_url + str(date_str) + '?edition=all&page=' + str(index)
        try:
            archive_soup =  requests.get(url)
        except:
            print("No response for links in archive,trying to reconnect")
            time.sleep(2)
            continue
        soup = BeautifulSoup(archive_soup.content, "html.parser")
        all_links = soup.find_all("a", attrs={"class": "link_overlay"})
        page_links_length = len(all_links)

        if(page_links_length == 0):
            break
        else:
            for link in all_links:
                link_separator = link.get('href').split('/')
                link = link_separator[1] + "/" +link_separator[2] + "/" + link_separator[3]
                output_file_name = 'bn_{}{}.txt'.format(link_separator[2],link_separator[3])
                article_url = newspaper_base_url + link
                try:
                    article_data = requests.get(article_url).text
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue
                with open(raw_output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                        file.write(str(article_url) + '\n' + str(article_data) )
                article_soup = BeautifulSoup(article_data, "html.parser")
                
                print(article_url)
                
                try:
                    article_info = article_soup.find_all("div", {"class": "additional_info_container"})
                    author = article_soup.find("div", {"class": "author"}).find("span", {"class": "name"}).text

                except:
                    author = ""

                try:
                    date_published = article_soup.find("span", {"itemprop": "datePublished"}).text
                except:
                    date_published = ""

                try:
                    tag_array = ""
                    article_tag = article_soup.find("strong", {"class": "topic_list"})
                    tags = article_soup.find("div", {"class": "topic_list"}).find_all("a")
                    for tag in tags:
                        tag_array += tag.text + " "
                except:
                    tag_array = ""

                article_content = article_soup.find_all("div", {"class": "content_detail"})
                article_title = article_soup.find("h1", {"class": "title"})
                article_body = article_soup.find("div", {"itemprop": "articleBody"})

                try:
             	    article_title_text = str(article_title.text.strip())
                except:
                    article_title_text = "" 
                try:
                    article_body_text = article_body.get_text(separator="\n\n")
                except:
                    article_body_text = ""

                data  =  "<article>\n"
                data +=  "<title>"      + article_title_text                            + "</title>\n"
                data +=  "<date>"       + date_published                                + "</date>\n"
                data +=  "<topic>"      + tag_array                                     + "</topic>\n"
                data +=  "<author>"     + author                                        + "</author>\n"
                data +=  "<text>"       + article_body_text                             + "</text>\n"
                data +=  "</article>"

                with open(output_dir+ '/' + output_file_name, 'w', encoding='utf8') as file:
                    file.write(data + '\n\n')