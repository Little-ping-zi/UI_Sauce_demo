import unittest
from ..utils.driver_manager import DriverManage
from ..pages.login_page import LoginPage
from ..pages.products_page import ProductsPage


class TestSauceDemo(unittest.TestCase):
    # def setUp(self):
    #     self.driver = DriverManage.get_driver()

    product_page = None
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = DriverManage.get_driver()
        login_page = LoginPage(cls.driver)
        cls.product_page = login_page.login("standard_user", "secret_sauce")

    def setUp(self) -> None:
        self.driver = self.__class__.driver
        self.product_page = self.__class__.product_page
        print(f'\n开始执行：{self._testMethodName}')

    @classmethod
    def tearDownClass(cls):
        DriverManage.quit_driver(cls.driver)

    @unittest.skip('跳过')
    def test_01_add_product_remove(self):
        self.product_page.sort(1)
        add_count = self.product_page.add_product_to_cart(5)
        cart_page = self.product_page.go_to_cart()
        remove_amount = cart_page.remove_all_cart()
        cart_page.continue_shopping()

        self.assertEqual(add_count, remove_amount, "添加的商品和移除的商品数量一致")

    @unittest.skip('跳过')
    def test_02_add_all_product_remove(self):
        # print(self.product_page)
        # product_page = ProductsPage(self.driver)
        self.product_page.sort(1)
        add_count = self.product_page.add_all_products_to_cart()
        cart_page = self.product_page.go_to_cart()
        remove_amount = cart_page.remove_all_cart()
        cart_page.continue_shopping()

        self.assertEqual(add_count, remove_amount, "添加的商品和移除的商品数量一致")

    def test_03_only_add(self):
        self.product_page.sort(1)
        initial_cart_count = self.product_page.get_cart_badge_count()
        self.product_page.add_product_to_cart(3)
        new_cart_badge_count = self.product_page.get_cart_badge_count()
        print(new_cart_badge_count)
        self.assertEqual(initial_cart_count+1, new_cart_badge_count,
                         f"购物车商品数量应该从{initial_cart_count}增加到{initial_cart_count+1}")


def run_tests_in_order():
    suite = unittest.TestSuite()

    suite.addTest(TestSauceDemo('test_01_add_product_remove'))
    # suite.addTest(TestSauceDemo('test_02_add_all_product_remove'))
    suite.addTest(TestSauceDemo('test_03_only_add'))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == "__main__":
    run_tests_in_order()
