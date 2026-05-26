import os,sys
import unittest
from time import sleep
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from public.modle.myunit import MyTest
from public.pageobjects.cart_page import CartPage
from public.pageobjects.product_page import ProductPage
from public.pageobjects.login_page import LoginPage
from public.modle.log import Log
from public.modle.getyaml import GetYaml
from config import setting

# 加载购物车测试数据
test_yaml_path = os.path.join(setting.TEST_DATA, 'cart_test_data.yaml')
yaml_loader = GetYaml(test_yaml_path)
test_data = yaml_loader._load()


class TestCart(MyTest):
    """
    购物车页面测试用例
    包含主流程和边界场景测试
    """
    
    def setUp(self):
        """每个测试方法执行前的准备工作"""
        super().setUp()
        # 只登录
        self.login()
        # 清空购物车（确保测试环境干净）
        self.clear_cart()
        # 确保在商品页面
        pp = ProductPage(self.driver)
        pp.open_products_page()
        sleep(1)
    
    def clear_cart(self):
        """清空购物车中的所有商品"""
        try:
            # 先跳转到购物车页面
            pp = ProductPage(self.driver)
            pp.go_to_cart()
            sleep(1)
            
            cp = CartPage(self.driver)
            
            # 循环移除所有商品
            while not cp.is_cart_empty():
                cp.remove_item_from_cart(0)
                sleep(0.5)
            
            Log.info("购物车已清空")
        except Exception as e:
            Log.warning(f"清空购物车时出错（可能购物车本来就是空的）: {str(e)}")
        finally:
            # 返回商品页面
            pp = ProductPage(self.driver)
            pp.open_products_page()
            sleep(1)

    def login(self, products=None):
        """
        登录系统
        """
        # 登录
        phone = 'standard_user'
        password = 'secret_sauce'
        LoginPage(self.driver).user_login(phone, password)

    def add_products(self, products=None):
        """
        添加商品到购物车（不跳转页面）
        :param products: 要添加的商品列表，默认为 ['backpack']
        """
        if products is None:
            products = ['backpack']
        Log.debug(f'需要添加到购物车的商品：{products}')
            
        # 确保在商品页面
        pp = ProductPage(self.driver)
            
        for product in products:
            Log.debug(f'添加商品：{product}')
            pp.add_product_to_cart(product)
            sleep(0.5)
        
    def go_to_cart_page(self):
        """跳转到购物车页面"""
        pp = ProductPage(self.driver)
        pp.go_to_cart()
        sleep(1)

    # ==================== 主流程测试用例 ====================

    def test_01_cart_page_loads_successfully(self):
        """
        【主流程】验证购物车页面能够成功加载
        步骤：
        1. 登录系统并添加商品
        2. 访问购物车页面
        3. 验证页面标题正确
        """
        self.add_products()
        # 跳转到购物车页面
        self.go_to_cart_page()

        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_01_cart_page_loads_successfully']
        data = case_data['data']
        check = case_data['check']

        cp = CartPage(self.driver)

        # 验证页面标题
        title = cp.get_page_title()
        Log.debug(f"购物车页面标题: {title}")
        self.assertEqual(title, check['page_title'],
                        f"页面标题应为'{check['page_title']}'，实际为'{title}'")

        Log.info(f"购物车页面加载成功，标题: {title}")

    def test_02_verify_added_product_in_cart(self):
        """
        【主流程】验证添加到购物车的商品正确显示
        步骤：
        1. 登录系统并添加商品
        2. 访问购物车页面
        3. 验证商品信息正确显示
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_02_verify_added_product_in_cart']
        data = case_data['data']
        check = case_data['check']

        # 添加商品到购物车（在测试用例中执行）
        self.add_products([data['product_name']])

        # 跳转到购物车页面
        self.go_to_cart_page()

        cp = CartPage(self.driver)

        # 验证购物车中有商品
        item_count = cp.get_cart_items_count()
        self.assertGreater(item_count, 0, "购物车中应该有商品")

        # 验证商品名称（统一转为小写比较）
        item_names = cp.get_cart_item_names()
        expected_name = data['product_name']
        actual_names = ' '.join(item_names).lower()
        Log.debug(f'购物车中商品名称：{actual_names}')
        self.assertIn(expected_name, actual_names,
                     f"购物车中应该包含商品 {data['product_name']}")

        Log.info(f"成功验证商品 {data['product_name']} 在购物车中")

    def test_03_remove_item_from_cart(self):
        """
        【主流程】验证可以从购物车移除商品
        步骤：
        1. 登录系统并添加多个商品
        2. 访问购物车页面
        3. 移除一个商品
        4. 验证商品已被移除
        """
        # 添加多个商品
        products = ['backpack', 'bike_light', 'bolt_shirt']
        self.add_products(products)

        # 跳转到购物车页面
        self.go_to_cart_page()

        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_03_remove_item_from_cart']
        data = case_data['data']
        check = case_data['check']

        cp = CartPage(self.driver)

        # 记录移除前的商品数量
        before_count = cp.get_cart_items_count()
        Log.info(f"移除前购物车商品数量: {before_count}")

        # 移除第一个商品
        cp.remove_item_from_cart(0)
        sleep(1)

        # 验证商品数量减少
        after_count = cp.get_cart_items_count()
        Log.info(f"移除后购物车商品数量: {after_count}")
        self.assertEqual(after_count, before_count - 1,
                        f"移除商品后数量应从 {before_count} 变为 {before_count - 1}")

        Log.info(f"成功从购物车移除商品，剩余 {after_count} 个商品")

    # ==================== 边界场景测试用例 ====================

    def test_04_multiple_items_in_cart(self):
        """
        边界测试：验证多个商品可以同时在购物车中
        步骤：
        1. 登录系统并添加多个商品
        2. 访问购物车页面
        3. 验证所有商品都显示
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_04_multiple_items_in_cart']
        data = case_data['data']
        check = case_data['check']

        # 添加多个商品
        products = data['products']
        self.add_products(products)

        # 跳转到购物车页面
        self.go_to_cart_page()

        cp = CartPage(self.driver)

        # 验证商品数量
        item_count = cp.get_cart_items_count()
        self.assertEqual(item_count, check['total_items'],
                        f"购物车中应该有 {check['total_items']} 个商品，实际有 {item_count} 个")

        Log.info(f"成功验证 {item_count} 个商品在购物车中")

    def test_05_continue_shopping_button(self):
        """
        边界测试：验证点击继续购物按钮返回商品页面
        步骤：
        1. 登录系统并添加商品
        2. 访问购物车页面
        3. 点击继续购物按钮
        4. 验证返回商品页面
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_05_continue_shopping_button']
        data = case_data['data']
        check = case_data['check']

        # 添加商品
        products = [data['product_name']]
        self.add_products(products)

        # 跳转到购物车页面
        self.go_to_cart_page()

        cp = CartPage(self.driver)

        # 点击继续购物
        cp.continue_shopping()
        sleep(1)

        # 验证 URL 包含 inventory.html
        current_url = self.driver.current_url
        self.assertIn(check['url_contains'], current_url,
                     f"应该返回商品页面，当前URL: {current_url}")

        Log.info("成功验证继续购物按钮功能")

    def test_06_empty_cart_state(self):
        """
        边界测试：验证空购物车的正确显示
        步骤：
        1. 登录系统但不添加商品
        2. 直接访问购物车页面
        3. 验证空购物车状态
        """
        # 只登录，不添加商品
        phone = 'standard_user'
        password = 'secret_sauce'
        LoginPage(self.driver).user_login(phone, password)

        # 直接访问购物车页面
        cp = CartPage(self.driver)
        cp.open_cart_page()
        sleep(1)

        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_06_empty_cart_state']
        data = case_data['data']
        check = case_data['check']

        # 验证购物车为空
        is_empty = cp.is_cart_empty()
        self.assertTrue(is_empty, "购物车应该为空")

        # 验证商品数量为 0
        item_count = cp.get_cart_items_count()
        self.assertEqual(item_count, 0, "空购物车商品数量应为 0")

        Log.info("成功验证空购物车状态")

    def test_07_checkout_button_functionality(self):
        """
        边界测试：验证点击结算按钮进入结算流程
        步骤：
        1. 登录系统并添加商品
        2. 访问购物车页面
        3. 点击结算按钮
        4. 验证进入结算页面
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_07_checkout_button_functionality']
        data = case_data['data']
        check = case_data['check']

        products = data['product_name']
        self.add_products([products])

        cp = CartPage(self.driver)
        self.go_to_cart_page()

        # 点击结算按钮
        cp.proceed_to_checkout()
        sleep(1)

        # 验证 URL 包含 checkout
        current_url = self.driver.current_url
        self.assertIn(check['url_contains'], current_url,
                     f"应该进入结算页面，当前URL: {current_url}")

        Log.info("成功验证结算按钮功能")


if __name__ == '__main__':
    unittest.main()
