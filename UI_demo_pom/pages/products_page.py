import time
from .cart_page import CartPage
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class ProductsPage(BasePage):
    SORT = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_LIST = (By.CLASS_NAME, 'inventory_list')
    INVENTORY_ITEMS = (By.CLASS_NAME, 'inventory_item')
    PRODUCT_NAME = (By.CLASS_NAME, 'inventory_item_name')
    PRODUCT_DESCRIBE = (By.CLASS_NAME, 'inventory_item_desc')
    PRODUCT_PRICE = (By.CLASS_NAME, 'inventory_item_price')
    ADD_BUTTON = (By.CLASS_NAME, 'btn_inventory')
    CART_ELEMENT = (By.CLASS_NAME, 'shopping_cart_link')
    CART_BADGE_COUNT = (By.CLASS_NAME, 'shopping_cart_badge')

    def __init__(self, driver):
        super().__init__(driver)

    def sort(self, index):
        time.sleep(2)
        dropdown_element = self.find_element(*self.SORT)
        dropdown = Select(dropdown_element)
        dropdown.select_by_index(index)
        time.sleep(2)

    def get_page_products(self):
        self.find_element(*self.INVENTORY_LIST)
        inventory_items = self.find_elements(*self.INVENTORY_ITEMS)
        return inventory_items

    def get_product_info(self, product_element):
        product_name = product_element.find_element(*self.PRODUCT_NAME).text
        product_describe = product_element.find_element(*self.PRODUCT_DESCRIBE).text
        product_price = product_element.find_element(*self.PRODUCT_PRICE).text
        return (f"name: {product_name}", f"describe: {product_describe}", f"price: {product_price}")

    def add_product_to_cart(self, index):
        page_products = self.get_page_products()
        if index < len(page_products):
            select_product = page_products[index]
            product_info = self.get_product_info(select_product)
            print(f"{product_info[0]}\n{product_info[1]}\n{product_info[2]}")
            time.sleep(2)
            add_button = select_product.find_element(*self.ADD_BUTTON)
            add_button.click()
            return True
        return False

    def add_all_products_to_cart(self):
        page_products = self.get_page_products()
        add_count = 0

        for index, product in enumerate(page_products, 1):
            try:
                print(f"第{index}个商品信息如下：")
                product_info = self.get_product_info(product)
                print(f"{product_info[0]}\n{product_info[1]}\n{product_info[2]}")
                time.sleep(2)
                add_button = product.find_element(*self.ADD_BUTTON)
                add_button.click()
                time.sleep(2)
                add_count += 1
            except Exception as e:
                print(f"添加第{index}个商品时报错：{e}")
        print(f"共添加了{add_count}个商品")
        return add_count

    def get_cart_badge_count(self):
        try:
            cart_badge_element = self.find_element(*self.CART_BADGE_COUNT)
            cart_badge_count = cart_badge_element.text
            print(cart_badge_count)
            return int(cart_badge_count)
        except:
            return 0

    def go_to_cart(self):
        self.click_element(*self.CART_ELEMENT)
        return CartPage(self.driver)
