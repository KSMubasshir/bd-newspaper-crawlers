# - * -coding: utf - 8 - * -
# encoding = utf8
import sys
import json
import time
import difflib
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
import os
from datetime import date, timedelta
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

link_set = set()
visited = set()


def loadLinks():
    global link_set
    global visited
    with open('all.txt', 'r') as file1:
        with open('visited.txt', 'r') as file2:
            visited = set(file2)
            link_set = set(file1).difference(file2)


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


def extract_data(article_soup, output_file_name):
    try:
        title = article_soup.find("h1", {"class", "entry-title"}).get_text().strip()
    except:
        title = ""

    try:
        article_content = article_soup.find("div", {"class": "entry-content"}).get_text().strip()
    except:
        article_content = ""

    data = "<article>\n"
    data += "<title>" + title + "</title>\n"
    data += "<text>\n" + article_content + "\n</text>\n"
    data += "</article>"

    output_dir = './Data/'
    raw_output_dir = './' + "Raw" + '/'

    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    try:
        os.makedirs(raw_output_dir)
    except OSError:
        pass

    try:
        with open(raw_output_dir + '/' + output_file_name, 'w', encoding="utf8") as file:
            file.write(str(article_soup))
    except:
        pass

    try:
        with open(output_dir + '/' + output_file_name, 'w', encoding="utf8") as file:
            file.write(data)
    except:
        pass


def start():
    session = None
    base_url = 'https://songramernotebook.com/'
    try:
        print(base_url)
        session = getData(base_url, session)
        soup = BeautifulSoup(session.page_source, "html.parser")
        visited.add(base_url)
        with open("visited.txt", "a", encoding="utf8") as visited_file:
            visited_file.write(base_url + "\n")
    except Exception as e:
        print(e)
        exit()

    all_links = soup.find_all("a")

    if len(all_links) == 0:
        exit()
    else:
        for link in all_links:
            lnk = link.get('href').strip()
            if lnk.startswith("https://songramernotebook.com"):
                pass
            else:
                continue
            link_set.add(lnk)
            with open("all.txt", "a", encoding="utf8") as all_file:
                all_file.write(lnk + "\n")

    restart()


def restart():
    session = None
    while len(link_set) > 0:
        url = link_set.pop().strip()
        visited.add(url)
        with open("visited.txt", "a", encoding="utf8") as visited_file:
            visited_file.write(url + "\n")
        link_tokens = url.split("/")
        session = getData(url, session)
        article_soup = BeautifulSoup(session.page_source, "html.parser")

        # article link
        if (len(link_tokens) == 5) and link_tokens[4].isnumeric() and ("archives" in link_tokens[3]):
            print(url)
            extract_data(article_soup, link_tokens[4])

        # page link
        else:
            new_links = article_soup.find_all("a")
            if len(new_links) == 0:
                pass
            else:
                for full_link in new_links:
                    link = full_link.get('href').strip()
                    if link.startswith("https://songramernotebook.com"):
                        pass
                    else:
                        continue
                    if link in visited:
                        continue
                    link_set.add(link)
                    with open("all.txt", "a", encoding="utf8") as all_file:
                        all_file.write(link + "\n")


if __name__ == '__main__':
    # start()
    loadLinks()
    restart()
