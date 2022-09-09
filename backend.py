from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By # to locate elements (By.XPATH, By.ID,...)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
import json



class sele():

    def __init__(self):

        with open('settings.json') as f:
            sett = json.load(f)

        if sett['browser'] == 'Chrome':
            self.browser = webdriver.Chrome(ChromeDriverManager().install())
        elif sett['browser'] == 'Firefox':
            self.browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif sett['browser'] == 'Opera':
            self.browser = webdriver.Opera(executable_path=OperaDriverManager().install())

    def get(self, link):
        self.browser.get(link)