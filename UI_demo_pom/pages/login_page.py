# 登录网站
from .base_page import BasePage
from .products_page import ProductsPage
from selenium.webdriver.common.by import By
import time


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.CLASS_NAME, 'submit-button')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get('https://www.saucedemo.com/')

    def login(self, username, password):
        self.send_keys(*self.USERNAME_INPUT, username)
        self.send_keys(*self.PASSWORD_INPUT, password)
        time.sleep(2)
        self.click_element(*self.LOGIN_BUTTON)
        return ProductsPage(self.driver)