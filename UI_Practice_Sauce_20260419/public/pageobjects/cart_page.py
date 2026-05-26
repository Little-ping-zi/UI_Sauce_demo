import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from public.pageobjects.base_page import BasePage
from selenium.webdriver.common.by import By
from public.modle.getyaml import GetYaml
from config import setting
from public.modle.log import Log

# 加载购物车页面 YAML 配置（只包含元素定位器）
test_yaml_path = os.path.join(setting.TEST_YAML, 'cart.yaml')
cart_elements = GetYaml(test_yaml_path)


class CartPage(BasePage):
    url = '/cart.html'
    
    def __init__(self, driver):
        super().__init__(driver)
        # 从 YAML 加载所有元素定位器（使用键名映射）
        self.elements = {
            # 操作按钮
            'continue_shopping': cart_elements.get_by_locator('continue_shopping'),
            'checkout': cart_elements.get_by_locator('checkout'),
            'remove_button': cart_elements.get_by_locator('remove_button'),
            
            # 验证元素
            'page_title': cart_elements.get_by_locator('page_title'),
            'cart_items': cart_elements.get_by_locator('cart_items'),
            'cart_quantity': cart_elements.get_by_locator('cart_quantity'),
            'cart_description': cart_elements.get_by_locator('cart_description'),
            'cart_price': cart_elements.get_by_locator('cart_price'),
            'empty_cart_message': cart_elements.get_by_locator('empty_cart_message'),
        }

    def open_cart_page(self):
        """打开购物车页面"""
        self.open()

    def get_cart_items_count(self):
        """获取购物车中商品数量"""
        elements = self.find_elements(*self.elements['cart_items'])
        return len(elements)

    def get_cart_item_names(self):
        """获取购物车中所有商品名称"""
        items = self.find_elements(*self.elements['cart_description'])
        return [item.text for item in items]

    def get_cart_item_prices(self):
        """获取购物车中所有商品价格"""
        prices = self.find_elements(*self.elements['cart_price'])
        return [price.text for price in prices]

    def remove_item_from_cart(self, index=0):
        """移除购物车中的商品，默认移除第一个"""
        remove_buttons = self.find_elements(*self.elements['remove_button'])
        if index < len(remove_buttons):
            remove_buttons[index].click()

    def continue_shopping(self):
        """继续购物，返回商品页面"""
        self.find_element(*self.elements['continue_shopping']).click()

    def proceed_to_checkout(self):
        """进入结算流程"""
        self.find_element(*self.elements['checkout']).click()

    def get_page_title(self):
        """获取页面标题"""
        return self.find_element(*self.elements['page_title']).text

    def is_cart_empty(self):
        """检查购物车是否为空"""
        try:
            # 检查商品列表中的商品项数量
            items = self.find_elements(*self.elements['cart_items'])
            return len(items) == 0
        except Exception as e:
            Log.warning(f"检查购物车状态时出错: {str(e)}")
            return True

