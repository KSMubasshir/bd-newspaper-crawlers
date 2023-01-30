import os
import json
import time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import time
from stem import Signal
from stem.control import Controller
import shutil
from random import uniform
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# from io import open

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="abhik")
        controller.signal(Signal.NEWNYM)


def getData(link, session=None):
    global TOR_SWITCH

    if not session:
        session = webdriver.Firefox()

    time.sleep(9)

    while True:
        try:
            session.get(link)
        except Exception as e:
            print(e)
            renew_tor_ip()
            session.quit()
            profile = webdriver.FirefoxProfile()
            profile.set_preference('network.proxy.type', 1)
            profile.set_preference('network.proxy.socks', '127.0.0.1')
            profile.set_preference('network.proxy.socks_port', 9050)
            profile.set_preference('permissions.default.image', 2)
            profile.set_preference('browser.link.open_newwindow', 1)
            session = webdriver.Firefox(profile)

            print("********Changing IP************")
            time.sleep(15)
            continue
        else:
            return session


newspaper_base_url = 'https://bigyan.org.in/'

output_result = []
data = []
exceptions = 0

session = None

for index in range(1, 8):
    for j in range(7):
        if j == 0:
            url = newspaper_base_url + "2020/page/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "2019/page/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "2018/page/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "2017/page/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "2016/page/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "2015/page/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "2014/page/" + str(index)

        print(url)

        try:
            session = getData(url, session)
        except Exception as e:
            print(str(e))
            print("No response for links in archive,trying to reconnect")
            time.sleep(2)
            continue

        soup = BeautifulSoup(session.page_source, "html.parser")

        name = url.split("/")
        name = name[3] + "_" + name[4] + "_" + name[5]
        try:
            with open("Data/" + name, 'w', encoding='utf8') as file:
                file.write(str(soup))
        except Exception as e:
            print(str(e))
            pass
        continue

        all_links = soup.find_all("a", attrs={"class": "title"})
        page_links_length = len(all_links)

        if (page_links_length == 0):
            break
        else:
            for link in all_links:
                link_separator = link.get('href')

                link = "https://www.kalerkantho.com" + link_separator[1:]
                article_url = link

                link_tokens = link_separator.split("/")

                year = link_tokens[3]
                month = link_tokens[4]
                day = link_tokens[5]

                output_file_name = link_tokens[2] + "_" + link_tokens[3] + "_" + link_tokens[4] + "_" + link_tokens[
                    5] + "_" + link_tokens[6]

                output_dir = './{}/{}/{}/bn'.format(year, month, day)
                raw_output_dir = '../' + "Raw" + '/' + "Kalerkantho" + '/' + output_dir

                try:
                    os.makedirs(output_dir)
                except OSError:
                    pass
                try:
                    os.makedirs(raw_output_dir)
                except OSError:
                    pass

                try:
                    session = getData(article_url, session)
                except:
                    print("No response for content in link,trying to reconnect")
                    time.sleep(2)
                    continue
                article_soup = BeautifulSoup(session.page_source, "html.parser")

                print(article_url)
                paragraphs = article_soup.find_all("p")

                length = len(paragraphs)

                i = 0

                article_content = ""
                for paragraph in paragraphs:
                    if i == 0:
                        date = paragraph.get_text().split("|")[2]
                    elif i > 3 and i <= length - 2:
                        article_content += paragraph.get_text() + "\n"
                    else:
                        pass
                    i = i + 1

                data = "<article>\n"
                # data +=  "<title>" + title + "</title>\n"
                data += "<date>" + date + "</date>\n"
                # data +=  "<author>" + author + "</author>\n"
                data += "<text>" + article_content + "</text>\n"
                data += "</article>"

                with open(output_dir + '/' + output_file_name, 'w', encoding='utf8') as file:
                    file.write(data)
