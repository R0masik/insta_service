"""Instagram API"""

import json
import requests
from time import sleep
import urllib.parse as urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from config import Config


class InstaService:
    AUTHORIZE_URL = 'oauth/authorize'
    ACCESS_TOKEN_URL = 'oauth/access_token'

    REDIRECT_URL = 'http://localhost:3000'

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.browser = webdriver.Chrome(Config.DRIVER_PATH, options=self.options)
        self.auth_code = None
        self.access_token = None

    def login(self):
        params = {
            'client_id': Config.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'response_type': 'code'
        }
        auth_url = Config.API_HOST + self.AUTHORIZE_URL + '?' + urlparse.urlencode(params)
        self.browser.get(auth_url)
        self.wait_loading(By.NAME, 'username')

        # login
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(Config.USERNAME)
        passwd_field = self.browser.find_element_by_name('password')
        passwd_field.send_keys(Config.PASSWORD)
        login_button = self.browser.find_elements_by_tag_name('button')[1]
        login_button.click()
        self.wait_loading(By.CLASS_NAME, 'auth_done')

        parsed_params = urlparse.urlparse(self.browser.current_url).query
        self.auth_code = urlparse.parse_qs(parsed_params)['code'][0]
        self.access_token = self.get_access_token(self.auth_code)

    def get_access_token(self, code):
        data = {
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URL,
            'code': code
        }
        token_url = Config.API_HOST + self.ACCESS_TOKEN_URL
        req = requests.post(token_url, data=data)
        return req.json()['access_token']

    def check_followers(self):
        pass
        # self.browser.get(Config.HOST + self.PROFILE_PAGE_URL + self.PAGE_INFO_URL)
        # req = requests.get(Config.HOST + self.PROFILE_PAGE_URL + self.PAGE_INFO_URL)
        # print(req.text)
        # from pprint import pprint
        # pprint(req.text)

        # self.wait_loading(By.XPATH, '//a[@href="/rm_v/followers/"]')

        # profile_button = self.browser.find_element_by_xpath('//a[@href="/rm_v/followers/"]')
        # profile_button.click()
        # self.wait_loading(By.XPATH, '//div[@role="dialog"]')
        #
        # followers_form = self.browser.find_element_by_xpath('//div[@role="dialog"]')
        # print(followers_form)

    def wait_loading(self, by_attr, value):
        WebDriverWait(self.browser, 5).until(
            expected_conditions.presence_of_element_located((by_attr, value))
        )

    def __del__(self):
        self.browser.close()
        pass


if __name__ == '__main__':
    inst = InstaService()
    inst.login()
    # inst.check_followers()
