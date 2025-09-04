from selenium.webdriver.chrome.service import Service
from selenium import webdriver


class DriverManage:
    @staticmethod
    def get_driver():
        service = Service(executable_path=r"D:\chromedriver\chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        return driver

    @staticmethod
    def quit_driver(driver):
        if driver:
            driver.quit()
