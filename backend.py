from time import sleep
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

        self.browser.minimize_window()

    def get(self, routin):
        self.browser.maximize_window()
        for i in routin:
            actions = i.split('|')
            k = 0
            while k < len(actions):
                print(actions[k])
                if actions[k] == 'go to':
                    k += 1
                    print(actions[k])
                    self.browser.get(actions[k])
                elif actions[k] == 'click':
                    k += 1
                    self.browser.find_element(By.XPATH, actions[k]).click()
                elif actions[k] == 'wait':
                    k += 1
                    sleep(int(actions[k]))

                elif actions[k] == 'quit':
                    self.browser.quit()
                    k += 1
                elif actions[k] == 'send keys':
                    k += 1
                    self.browser.find_element(By.XPATH, actions[k]).send_keys(actions[k+1])
                k+=1