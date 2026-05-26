import configparser
import os,sys
from selenium.common import TimeoutException
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from public.modle.myunit import MyTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import setting
from public.modle.log import Log

con = configparser.ConfigParser()
con.read(setting.CONFIG, encoding='utf-8')
login_url = con.get('WebURL', 'URL')

class BasePage(MyTest):
    def __init__(self, driver, base_url=login_url):
        self.base_url = base_url
        self.driver = driver

    def _open(self, url):
        url = self.base_url + url
        Log.debug(f'需要访问的url: {url}')
        self.driver.get(url)

    def open(self):
        Log.debug(f'页面url: {self.url}')
        return self._open(self.url)

    def find_element(self, *loc):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(loc))
        except TimeoutException:
            return []
        return self.driver.find_elements(*loc)

    def send_keys(self, loc, value):
        return self.driver.find_element(*loc).send_keys(value)