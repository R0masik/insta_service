"""Instagram API"""

import json
import requests
from time import sleep
from bs4 import BeautifulSoup

from config import Config


class InstaService:
    AUTHORIZE_URL = 'oauth/authorize'
    ACCESS_TOKEN_URL = 'oauth/access_token'
    PROFILE_PAGE_URL = f'/{Config.USERNAME}/'
    REDIRECT_URL = 'http://localhost:3000'

    def __init__(self):
        auth_url = Config.API_HOST + self.AUTHORIZE_URL
        params = {
            'client_id': Config.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'response_type': 'code'
        }
        req = requests.get(auth_url, params=params)
        print(req.url)
        sleep(2)
        parser = BeautifulSoup(req.text, 'html.parser')
        t = parser.find_all('input', {'name': 'username'})
        print(t)
        print(req.text)

    def login(self):
        token_url = Config.API_HOST + self.ACCESS_TOKEN_URL
        params = {
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URL,
            'code': Config.CODE
        }
        print(token_url)
        req = requests.get(token_url, params=params)
        print(req.url)
        print(req.text)

    def check_followers(self):
        # self.browser.get(Config.HOST + self.PROFILE_PAGE_URL + self.PAGE_INFO_URL)
        req = requests.get(Config.HOST + self.PROFILE_PAGE_URL + self.PAGE_INFO_URL)
        print(req.text)
        # from pprint import pprint
        # pprint(req.text)

        # self.wait_loading(By.XPATH, '//a[@href="/rm_v/followers/"]')

        # profile_button = self.browser.find_element_by_xpath('//a[@href="/rm_v/followers/"]')
        # profile_button.click()
        # self.wait_loading(By.XPATH, '//div[@role="dialog"]')
        #
        # followers_form = self.browser.find_element_by_xpath('//div[@role="dialog"]')
        # print(followers_form)


if __name__ == '__main__':
    inst = InstaService()
    # inst.login()
    # inst.check_followers()
