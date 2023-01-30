import time
import os
import re
import pickle
import json
import copy
import shutil
import constants
import traceback
from random import uniform
from tqdm import tqdm
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class SessionBase(object):
    def __init__(self, max_download_delay):
        self.session = None
        self.max_download_delay = max_download_delay

    def open_new_session(self, *args, **kwargs):
        raise NotImplementedError()

    def get(self, url):
        raise NotImplementedError()

    def quit(self):
        raise NotImplementedError()

    def request(self, url, max_attempts=constants.MAX_RETRIES):
        rand = uniform(0, self.max_download_delay)
        for _ in range(max_attempts):
            try:
                self.get(url)
                time.sleep(rand)
            except:
                try:
                    self.open_new_session()
                except:
                    pass
            else:
                return


class TouchVPNSession(SessionBase):
    def __init__(self, max_download_delay, firefox_profile_dir, touchvpn_loc, start_with_vpn=False):
        super(TouchVPNSession, self).__init__(max_download_delay)
        self.firefox_profile_dir = firefox_profile_dir
        self.touchvpn_loc = touchvpn_loc
        self.open_new_session(start_with_vpn)

    def open_new_session(self, with_vpn=True):
        self.quit()

        if with_vpn:
            profile = webdriver.FirefoxProfile(self.firefox_profile_dir)
            profile.set_preference("dom.push.enabled", False)
            self.session = webdriver.Firefox(profile)
            self.session.maximize_window()

            try:
                self.session.get(self.touchvpn_loc)
                time.sleep(5)

                try:
                    # assume VPN is disconnected
                    self.session.find_element_by_xpath("//div[@id='ConnectionButton'][@class='disconnected']").click()
                except:
                    # VPN is connected; disconnect first
                    self.session.find_element_by_xpath("//div[@id='ConnectionButton'][@class='postConnection']").click()
                    WebDriverWait(self.session, 50).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@id='ConnectionButton'][@class='disconnected']")
                        )
                    )
                    # connect again
                    self.session.find_element_by_xpath("//div[@id='ConnectionButton'][@class='disconnected']").click()
                finally:
                    WebDriverWait(self.session, 50).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@id='ConnectionButton'][@class='postConnection']")
                        )
                    )
            except:
                self.quit()
                # fall back to regular connection
                pass
            else:
                # Successfully connected to VPN
                time.sleep(5)
                return

        profile = webdriver.FirefoxProfile(self.firefox_profile_dir)
        profile.set_preference("dom.push.enabled", False)
        self.session = webdriver.Firefox(profile)
        self.session.maximize_window()

    def get(self, url):
        self.session.get(url)

    def quit(self):
        if self.session:
            self.session.quit()


class TorSeleniumSession(SessionBase):
    def __init__(self, max_download_delay, firefox_profile_dir, password, start_with_tor=False):
        super(TorSeleniumSession, self).__init__(max_download_delay)
        self.firefox_profile_dir = firefox_profile_dir
        self.tor_profile = self.get_tor_profile()
        self.password = password
        self.open_new_session(start_with_tor)

    def get_tor_profile(self):
        profile = webdriver.FirefoxProfile(self.firefox_profile_dir)
        profile.set_preference("dom.push.enabled", False)
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9050)
        profile.set_preference('permissions.default.image', 2)
        profile.set_preference('browser.link.open_newwindow', 1)

        return profile

    def renew_tor_ip(self):
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)

    def open_new_session(self, with_tor=True):
        self.quit()

        if with_tor:
            self.session = webdriver.Firefox(self.get_tor_profile())
            self.session.maximize_window()
            self.renew_tor_ip()
            time.sleep(15)
            return

        profile = webdriver.FirefoxProfile(self.firefox_profile_dir)
        self.session = webdriver.Firefox(profile)
        self.session.maximize_window()

    def get(self, url):
        self.session.get(url)

    def quit(self):
        if self.session:
            self.session.quit()

# TODO: Write a wrapper using requests
