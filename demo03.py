from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path=r'D:\chromedriver\chromedriver.exe')

driver = webdriver.Chrome(service=service)
# driver.implicitly_wait(10)
driver.get('https://console.whaee.com/v2/login')

driver.find_element(By.NAME, 'username').send_keys('17674073370')
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[2]/div/form/div[2]/div/div[1]/input').send_keys('123456')
driver.find_element(By.CLASS_NAME, 'wsw-sign-submit').click()

time.sleep(15)



driver.quit()