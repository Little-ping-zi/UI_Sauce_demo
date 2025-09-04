import time
from .base_page import BasePage
from selenium.webdriver.common.by import By


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        super().__init__(driver)

    def checkout_info_input(self, first_name, last_name, postal_code):
        self.send_keys(*self.FIRST_NAME, first_name)
        self.send_keys(*self.LAST_NAME, last_name)
        self.send_keys(*self.POSTAL_CODE, postal_code)
        time.sleep(2)

    def checkout_finish(self):
        self.click_element(*self.CONTINUE_BUTTON)
        finish_element = self.click_element(*self.FINISH_BUTTON)
        complete_header = finish_element.find_element(*self.COMPLETE_HEADER).text
        time.sleep(2)
        return complete_header
