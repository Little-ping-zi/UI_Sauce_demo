import unittest
from ..utils.driver_manager import DriverManage
from ..pages.login_page import LoginPage


class AddRemove(unittest.TestCase):
    def setUp(self):
        self.driver = DriverManage.get_driver()

    def tearDown(self):
        DriverManage.quit_driver(self.driver)

    def test_add_remove(self):
        login_page = LoginPage(self.driver)
        product_page = login_page.login("standard_user", "secret_sauce")
        product_page.sort(1)
        add_count = product_page.add_all_products_to_cart()
        cart_page = product_page.go_to_cart()
        remove_amount = cart_page.remove_all_cart()

        self.assertEqual(add_count, remove_amount, "添加的商品和移除的商品数量一致")


if __name__ == "__main__":
    unittest.main()