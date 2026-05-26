import os,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from public.pageobjects.base_page import BasePage
from public.modle.getyaml import GetYaml
from config import setting
from public.modle.log import Log

# 加载商品页面YAML配置
test_yaml_path = os.path.join(setting.TEST_YAML, 'product.yaml')
testyaml = GetYaml(test_yaml_path)


class ProductPage(BasePage):
    url = '/inventory.html'
    
    def __init__(self, driver):
        super().__init__(driver)
        # 从 YAML 加载所有元素定位器（使用键名映射）
        self.elements = {
            # 添加商品按钮
            'backpack_add': testyaml.get_by_locator('backpack_add'),
            'bike_light_add': testyaml.get_by_locator('bike_light_add'),
            'bolt_shirt_add': testyaml.get_by_locator('bolt_shirt_add'),
            'fleece_jacket_add': testyaml.get_by_locator('fleece_jacket_add'),
            'onesie_add': testyaml.get_by_locator('onesie_add'),
            'red_tshirt_add': testyaml.get_by_locator('red_tshirt_add'),
            
            # 移除商品按钮
            'backpack_remove': testyaml.get_by_locator('backpack_remove'),
            'bike_light_remove': testyaml.get_by_locator('bike_light_remove'),
            'bolt_shirt_remove': testyaml.get_by_locator('bolt_shirt_remove'),
            'fleece_jacket_remove': testyaml.get_by_locator('fleece_jacket_remove'),
            'onesie_remove': testyaml.get_by_locator('onesie_remove'),
            'red_tshirt_remove': testyaml.get_by_locator('red_tshirt_remove'),
            
            # 其他操作元素
            'cart_link': testyaml.get_by_locator('cart_link'),
            
            # 验证元素
            'page_title': testyaml.get_by_locator('page_title'),
            'inventory_items': testyaml.get_by_locator('inventory_items'),
        }

    def open_products_page(self):
        """打开商品页面"""
        self.open()

    def add_product_to_cart(self, product_name):
        """添加指定商品到购物车"""
        element_key = f'{product_name}_add'
        Log.debug(f'需要添加到购物车的商品：{element_key}')
        if element_key in self.elements:
            self.find_element(*self.elements[element_key]).click()
        else:
            raise ValueError(f"Unknown product: {product_name}")

    def remove_product_from_cart(self, product_name):
        """从购物车移除指定商品"""
        element_key = f'{product_name}_remove'
        if element_key in self.elements:
            self.find_element(*self.elements[element_key]).click()
        else:
            raise ValueError(f"Unknown product: {product_name}")

    def go_to_cart(self):
        """跳转到购物车页面"""
        self.find_element(*self.elements['cart_link']).click()

    def get_page_title(self):
        """获取页面标题"""
        return self.find_element(*self.elements['page_title']).text

    def get_product_count(self):
        """获取商品总数"""
        products = self.find_elements(*self.elements['inventory_items'])
        return len(products)

    def is_product_displayed(self, product_name):
        """检查指定商品的按钮是否显示（添加或移除按钮）"""
        try:
            # 先检查移除按钮是否可见（商品已添加到购物车）
            remove_key = f'{product_name}_remove'
            if remove_key in self.elements:
                try:
                    remove_element = self.find_element(*self.elements[remove_key])
                    if remove_element.is_displayed():
                        return True
                except:
                    pass
            
            # 再检查添加按钮是否可见（商品未添加到购物车）
            add_key = f'{product_name}_add'
            if add_key in self.elements:
                add_element = self.find_element(*self.elements[add_key])
                return add_element.is_displayed()
            
            return False
        except:
            return False

    def is_product_added_to_cart(self, product_name):
        """检查商品是否已添加到购物车（移除按钮可见）"""
        try:
            remove_key = f'{product_name}_remove'
            if remove_key in self.elements:
                remove_element = self.find_element(*self.elements[remove_key])
                is_displayed = remove_element.is_displayed()
                Log.debug(f"商品 {product_name} 的移除按钮状态: {is_displayed}")
                return is_displayed
            Log.warning(f"商品 {product_name} 的移除按钮配置不存在: {remove_key}")
            return False
        except Exception as e:
            Log.error(f"检查商品 {product_name} 是否已添加时出错: {str(e)}")
            return False

    def is_product_available_to_add(self, product_name):
        """检查商品是否可以添加到购物车（添加按钮可见）"""
        try:
            add_key = f'{product_name}_add'
            if add_key in self.elements:
                add_element = self.find_element(*self.elements[add_key])
                return add_element.is_displayed()
            return False
        except:
            return False