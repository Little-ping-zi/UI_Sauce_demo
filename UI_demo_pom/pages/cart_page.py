import time
from .base_page import BasePage
from .checkout_page import CheckoutPage
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    REMOVE_BUTTON = (By.CLASS_NAME, 'cart_button')
    CHECKOUT_BUTTON = (By.CLASS_NAME, 'checkout_button')
    CONTINUE_SHOPPING = (By.ID, 'continue-shopping')

    def remove_all_cart(self):
        remove_buttons = self.find_elements(*self.REMOVE_BUTTON)
        print(f"购物车共{len(remove_buttons)}个商品")
        remove_count = 0
        for index, remove_button in enumerate(remove_buttons, 1):
            try:
                remove_button.click()
                print(f"已移除第{index}个商品")
                remove_count += 1
                time.sleep(2)
            except Exception as e:
                print(f"移除第{index}个商品时出错：e")

        print(f"所有商品已从购物车移除")
        return remove_count

    def go_to_checkout(self):
        time.sleep(2)
        self.click_element(*self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver)

    def continue_shopping(self):
        self.click_element(*self.CONTINUE_SHOPPING)
        from .products_page import ProductsPage
        return ProductsPage(self.driver)
