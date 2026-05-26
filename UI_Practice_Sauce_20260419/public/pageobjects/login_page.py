import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from public.pageobjects.base_page import BasePage
from selenium.webdriver.common.by import By
from public.modle.getyaml import GetYaml
from config import setting
from public.modle.log import Log

test_yaml_path = os.path.join(setting.TEST_YAML, 'login.yaml')
testyaml = GetYaml(test_yaml_path)

class LoginPage(BasePage):
    url = '/'

    # _username_input_loc = (By.ID, 'user-name')
    # _password_input_loc = (By.ID, 'password')
    # _login_button_loc = (By.CLASS_NAME, 'submit-button')
    # _menu_button_loc = (By.ID, 'react-burger-menu-btn')
    # _logout_loc = (By.ID, 'logout_sidebar_link')
    _username_input_loc = (By.ID, testyaml.get_element_info(0))
    _password_input_loc = (By.ID, testyaml.get_element_info(1))
    _login_button_loc = (By.CLASS_NAME, testyaml.get_element_info(2))
    _menu_button_loc = (By.ID, testyaml.get_element_info(3))
    _logout_loc = (By.ID, testyaml.get_element_info(4))
    _dashboard_text_loc = (By.CLASS_NAME, testyaml.get_check_element_info(0))
    _locked_out_hit_loc = (By.XPATH, testyaml.get_check_element_info(1))


    def login_phone(self, phone):
        self.send_keys(self._username_input_loc, phone)

    def login_password(self, password):
        self.send_keys(self._password_input_loc, password)

    def login_button(self):
        self.find_element(*self._login_button_loc).click()

    def logout(self):
        self.find_element(*self._menu_button_loc).click()
        self.find_element(*self._logout_loc).click()

    def user_login(self, phone, password):
        Log.info('执行登录操作')
        self.open()
        self.login_phone(phone)
        self.login_password(password)
        self.login_button()

    def user_logout(self):
        self.logout()

    def login_success_hint(self):
        return self.find_element(*self._dashboard_text_loc).text

    def login_locked_out_hit(self):
        # print(self._locked_out_hit_loc)
        # element = self.find_element(*self._locked_out_hit_loc)
        # text = element.text
        # print(text)
        return self.find_element(*self._locked_out_hit_loc).text

