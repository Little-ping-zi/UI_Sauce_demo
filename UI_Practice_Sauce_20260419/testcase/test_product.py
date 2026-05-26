import os,sys
import unittest
from time import sleep
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from public.modle.myunit import MyTest
from public.pageobjects.product_page import ProductPage
from public.pageobjects.login_page import LoginPage
from public.modle.log import Log
from public.modle.getyaml import GetYaml
from config import setting

# 直接使用 GetYaml 加载测试数据
test_yaml_path = os.path.join(setting.TEST_DATA, 'product_test_data.yaml')
yaml_loader = GetYaml(test_yaml_path)
# 获取所有测试数据
test_data = yaml_loader._load()

class TestProduct(MyTest):
    """
    商品详情页测试用例
    包含主流程和边界场景测试
    """
    
    def setUp(self):
        """每个测试方法执行前的准备工作"""
        super().setUp()
        # 登录到系统
        self.login()

    def login(self):
        """使用标准用户登录"""
        phone = 'standard_user'
        password = 'secret_sauce'
        LoginPage(self.driver).user_login(phone, password)

    # ==================== 主流程测试用例 ====================
    
    def test_01_product_page_loads_successfully(self):
        """
        【主流程】验证商品页面能够成功加载
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 验证页面标题正确
        4. 验证商品列表存在
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_01_product_page_loads_successfully']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()
        
        # 验证页面标题
        title = pp.get_page_title()
        Log.debug(f"页面标题: {title}")
        self.assertEqual(title, check['page_title'], 
                        f"页面标题应为'{check['page_title']}'，实际为'{title}'")
        
        # 验证商品数量大于0
        product_count = pp.get_product_count()
        self.assertGreater(product_count, check['min_product_count'] - 1, 
                          "商品列表中应该有商品")
        
        Log.info(f"商品页面加载成功，共有 {product_count} 个商品")

    def test_02_add_single_product_to_cart(self):
        """
        【主流程】验证单个商品可以成功添加到购物车
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 添加一个商品到购物车
        4. 验证添加按钮变为移除按钮
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_02_add_single_product_to_cart']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()

        # 从 YAML 获取商品名称
        product_name = data['product_name']
        
        # 添加商品到购物车
        pp.add_product_to_cart(product_name)

        # 验证添加按钮已变为移除按钮
        is_added = pp.is_product_added_to_cart(product_name)
        self.assertTrue(is_added, "添加商品后，移除按钮应该可见")

        Log.info(f"成功添加单个商品 {product_name} 到购物车")

    def test_03_add_multiple_products_to_cart(self):
        """
        【主流程】验证多个商品可以成功添加到购物车
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 添加多个商品到购物车
        4. 验证所有商品都已添加
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_03_add_multiple_products_to_cart']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()

        # 从 YAML 获取商品列表
        products_to_add = data['products']
        
        for product in products_to_add:
            Log.info(f"正在添加商品: {product}")
            pp.add_product_to_cart(product)
            sleep(1)

        # 验证所有商品都已添加
        for product in products_to_add:
            is_added = pp.is_product_added_to_cart(product)
            Log.info(f"商品 {product} 添加状态: {is_added}")
            self.assertTrue(is_added, f"商品 {product} 应该已添加到购物车")

        Log.info(f"成功添加 {len(products_to_add)} 个商品到购物车")

    # ==================== 边界场景测试用例 ====================

    def test_04_remove_product_from_cart(self):
        """
        边界测试：验证可以从购物车移除商品
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 添加商品到购物车
        4. 移除商品
        5. 验证移除按钮变回添加按钮
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_04_remove_product_from_cart']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()

        # 从 YAML 获取商品名称
        product_name = data['product_name']
        
        # 先添加商品
        pp.add_product_to_cart(product_name)
        sleep(0.5)

        # 再移除商品
        pp.remove_product_from_cart(product_name)
        sleep(0.5)

        # 验证移除后添加按钮重新出现
        can_add = pp.is_product_available_to_add(product_name)
        self.assertTrue(can_add, "移除商品后，添加按钮应该重新可见")

        Log.info(f"成功从购物车移除商品 {product_name}")

    def test_05_navigate_to_cart_from_product_page(self):
        """
        边界测试：验证可以从商品页面跳转到购物车页面
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 添加商品到购物车
        4. 点击购物车图标
        5. 验证成功跳转到购物车页面
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_05_navigate_to_cart_from_product_page']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()

        # 从 YAML 获取商品名称
        product_name = data['product_name']
        
        # 添加商品到购物车
        pp.add_product_to_cart(product_name)
        sleep(0.5)

        # 跳转到购物车页面
        pp.go_to_cart()
        sleep(1)

        # 从 YAML 获取预期 URL
        expected_url_part = check['url_contains']
        current_url = self.driver.current_url
        self.assertIn(expected_url_part, current_url, 
                     f"应该跳转到购物车页面，当前URL: {current_url}")

        Log.info("成功从商品页面跳转到购物车页面")

    def test_06_all_products_are_displayed(self):
        """
        边界测试：验证所有商品都正确显示
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 验证每个商品都可见
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_06_all_products_are_displayed']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()

        # 从 YAML 获取所有商品列表
        all_products = data['expected_products']
        displayed_count = 0

        for product in all_products:
            if pp.is_product_displayed(product):
                displayed_count += 1

        self.assertEqual(displayed_count, check['total_count'],
                        f"应该显示 {check['total_count']} 个商品，实际显示 {displayed_count} 个")

        Log.info(f"所有 {displayed_count} 个商品都正确显示")

    def test_07_product_page_title_verification(self):
        """
        边界测试：验证商品页面标题正确性
        步骤：
        1. 登录系统
        2. 访问商品页面
        3. 验证页面标题为'Products'
        """
        # 从 YAML 获取测试数据
        case_data = test_data['test_cases']['test_07_product_page_title_verification']
        data = case_data['data']
        check = case_data['check']
        
        pp = ProductPage(self.driver)
        pp.open_products_page()

        # 从 YAML 获取预期标题
        expected_title = check['page_title']
        title = pp.get_page_title()
        self.assertEqual(title, expected_title, 
                        f"页面标题应为'{expected_title}'，实际为'{title}'")

        Log.info(f"页面标题验证通过: {title}")

if __name__=='__main__':
    unittest.main()

