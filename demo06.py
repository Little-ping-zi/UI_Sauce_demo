from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

service = Service(executable_path=r'D:\chromedriver\chromedriver.exe')

driver = webdriver.Chrome(service=service)
# driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)
driver.get('https://www.saucedemo.com/')

# 登录网站
driver.find_element(By.ID, 'user-name').send_keys('standard_user')
driver.find_element(By.ID, 'password').send_keys('secret_sauce')
driver.find_element(By.CLASS_NAME, 'submit-button').click()

# 添加商品到购物车
dropdown_element = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "product_sort_container"))
)
dropdown = Select(dropdown_element)
dropdown.select_by_index(1)

inventory_list = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'inventory_list'))
)
inventory_items = driver.find_elements(By.CLASS_NAME, 'inventory_item')
print(f"{inventory_list}\n{inventory_items}")
# 添加一个商品到购物车
second_inventory = inventory_items[1]
product_name = second_inventory.find_element(By.CLASS_NAME, 'inventory_item_name').text
product_describe = second_inventory.find_element(By.CLASS_NAME, 'inventory_item_desc').text
product_price = second_inventory.find_element(By.CLASS_NAME, 'inventory_item_price').text
print(f"{product_name}\n{product_describe}\n{product_price}")
second_inventory.find_element(By.CLASS_NAME, 'btn_inventory').click()
# badge_count = second_inventory.find_element(By.CLASS_NAME, 'shopping_cart_badge')
badge_count = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, 'shopping_cart_badge'))
)
print(badge_count.text)
# 添加多个商品到购物车
# for index, inventory in enumerate(inventory_items, 1):
#     print(f"第{index}个商品的信息如下：")
#     product_name = inventory.find_element(By.CLASS_NAME, 'inventory_item_name ').text
#     product_describe = inventory.find_element(By.CLASS_NAME, 'inventory_item_desc').text
#     product_price = inventory.find_element(By.CLASS_NAME, 'inventory_item_price').text
#     print(f"{product_name}\n{product_describe}\n{product_price}")
#     inventory.find_element(By.CLASS_NAME, 'btn_inventory').click()
#     time.sleep(2)
# print(f"共添加了{len(inventory_items)}个商品到购物车")

# 从购物车移除商品
# cart = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
# cart.click()
#
# wait.until(
#     EC.element_to_be_clickable((By.CLASS_NAME, 'cart_button'))
# )
# remove_list = driver.find_elements(By.CLASS_NAME, 'cart_button')
# print(f"购物车共{len(remove_list)}个商品")
#
# for index, button in enumerate(remove_list, 1):
#     try:
#         time.sleep(2)
#         button.click()
#         print(f"已移除第{index}个商品")
#     except Exception as e:
#         print(f"移除第{index}个商品时出错: {e}")
# print("所有商品已从购物车移除")

time.sleep(5)

driver.quit()


