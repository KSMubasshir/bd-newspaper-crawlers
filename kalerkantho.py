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


newspaper_base_url = 'https://www.kalerkantho.com/online/'

output_result = []
data = []
exceptions = 0

session = None

for i in range(5927):
    index = i * 18

    for j in range(15):
        if j == 0:
            url = newspaper_base_url + "national/" + str(index)
        elif j == 1:
            url = newspaper_base_url + "country-news/" + str(index)
        elif j == 2:
            url = newspaper_base_url + "world/" + str(index)
        elif j == 3:
            url = newspaper_base_url + "entertainment/" + str(index)
        elif j == 4:
            url = newspaper_base_url + "sport/" + str(index)
        elif j == 5:
            url = newspaper_base_url + "business/" + str(index)
        elif j == 6:
            url = newspaper_base_url + "miscellaneous/" + str(index)
        elif j == 7:
            url = newspaper_base_url + "reporters-diary/" + str(index)
        elif j == 8:
            url = newspaper_base_url + "readers-place/" + str(index)
        elif j == 9:
            url = newspaper_base_url + "lifestyle/" + str(index)
        elif j == 10:
            url = newspaper_base_url + "info-tech/" + str(index)
        elif j == 11:
            url = newspaper_base_url + "nrb/" + str(index)
        elif j == 12:
            url = newspaper_base_url + "viral/" + str(index)
        elif j == 13:
            url = newspaper_base_url + "corporatecorner/" + str(index)
        else:
            url = newspaper_base_url + "book-fair/" + str(index)

        print(url)

        try:
            session = getData(url, session)
        except:
            print("No response for links in archive,trying to reconnect")
            time.sleep(2)
            continue

        soup = BeautifulSoup(session.page_source, "html.parser")

        all_links = soup.find_all("a", attrs={"class": "title"})
        page_links_length = len(all_links)

        if page_links_length == 0:
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
