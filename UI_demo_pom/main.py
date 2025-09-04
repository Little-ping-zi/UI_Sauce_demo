import time

from utils.driver_manager import DriverManage
from pages.login_page import LoginPage


def main():
    driver = None
    try:
        driver = DriverManage.get_driver()

        login_page = LoginPage(driver)
        products_page = login_page.login("standard_user", "secret_sauce")

        products_page.sort(1)
        products_page.add_product_to_cart(2)
        # products_page.add_all_products_to_cart()
        cart_page = products_page.go_to_cart()
        # cart_page.remove_all_cart()
        checkout_page = cart_page.go_to_checkout()
        checkout_page.checkout_info_input('a', 'b', 'c')
        checkout_page.checkout_finish()

        print(f"测试流程执行完毕！")
    except Exception as e:
        print(f"测试流程执行失败：{e}")

    finally:
        if driver:
            DriverManage.quit_driver(driver)

if __name__ == "__main__":
        main()





