"""Instagram API"""

import json
import requests
import urllib.parse as urlparse

import pyotp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from config import Config


class InstaService:
    AUTHORIZE = 'oauth/authorize'
    ACCESS_TOKEN = 'oauth/access_token'
    FOLLOWERS = lambda self, user_id: f'v1/users/{user_id}/follows'

    REDIRECT = 'http://localhost:3000'

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.browser = webdriver.Chrome(Config.DRIVER_PATH, options=self.options)
        self.auth_code = None
        self.access_token = None
        self.user_id = None

    def login(self):
        params = {
            'client_id': Config.CLIENT_ID,
            'redirect_uri': self.REDIRECT,
            'response_type': 'code',
            'scope': 'user_profile,user_media'
        }
        auth_url = Config.API_HOST + self.AUTHORIZE + '?' + urlparse.urlencode(params)
        self.browser.get(auth_url)
        self.wait_loading(By.NAME, 'username')

        # login
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(Config.USERNAME)
        passwd_field = self.browser.find_element_by_name('password')
        passwd_field.send_keys(Config.PASSWORD)
        login_button = self.browser.find_elements_by_tag_name('button')[1]
        login_button.click()
        self.wait_loading(By.ID, 'verificationCodeDescription')

        # two-factor authentication
        code_field = self.browser.find_element_by_name('verificationCode')
        code = self.otp_code()
        code_field.send_keys(code)
        confirm_button = self.browser.find_elements_by_tag_name('button')[0]
        confirm_button.click()
        self.wait_loading(By.CLASS_NAME, 'auth_done')

        parsed_params = urlparse.urlparse(self.browser.current_url).query
        self.auth_code = urlparse.parse_qs(parsed_params)['code'][0]

        access_token_resp = self.get_access_token(self.auth_code)
        self.access_token = access_token_resp['access_token']
        self.user_id = access_token_resp['user']['id']

    def otp_code(self):
        return pyotp.TOTP(Config.AUTH_KEY).now()

    def get_access_token(self, code):
        data = {
            'client_id': Config.CLIENT_ID,
            'client_secret': Config.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT,
            'code': code
        }
        token_url = Config.API_HOST + self.ACCESS_TOKEN
        req = requests.post(token_url, data=data)
        print(req.json())
        return req.json()

    def check_followers(self):
        followers_url = Config.API_HOST + self.FOLLOWERS(self.user_id)
        params = {'access_token': self.access_token,
                  }

        print(followers_url)
        followers_resp = requests.get(followers_url, params=params)

        from pprint import pprint
        pprint(followers_resp.json())

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
    inst.check_followers()
