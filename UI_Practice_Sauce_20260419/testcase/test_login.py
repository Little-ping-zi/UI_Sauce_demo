import os, sys, ddt
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from time import sleep
import yaml
import unittest
from public.modle.myunit import MyTest
from public.pageobjects.login_page import LoginPage
from config import setting
from public.modle import screenshot
from public.modle.log import Log

test_data_path = os.path.join(setting.TEST_DATA, 'login_data.yaml')
with open(test_data_path, encoding='utf-8') as f:
    testData = yaml.safe_load(f)


@ddt.ddt
class TestLogin(MyTest):
    @ddt.data(*testData)
    def test_login(self, loginyaml):
        """
        登录测试用例
        
        截图策略说明：
        1. tearDown中会自动捕获失败截图（兜底保障）
        2. 此处手动截图用于记录业务关键节点（断言前的页面状态）
        3. 两者互补：手动截图有业务语义，自动截图保证不遗漏
        """
        phone = loginyaml['data']['phone']
        password = loginyaml['data']['password']
        screenshot_name = loginyaml['screenshot']
        screenshot_file_name = screenshot_name + '.png'
        lp = LoginPage(self.driver)
        lp.user_login(phone, password)
        if screenshot_name == 'login_locked':
            login_check_hint = lp.login_locked_out_hit()
        else:
            login_check_hint = lp.login_success_hint()
        
        # 【手动截图】记录业务验证前的页面状态（有业务语义的截图）
        # 这种截图即使测试通过也会保存，用于后续审查或报告
        screenshot.insert_img(self.driver, screenshot_file_name)
        Log.info(f'已保存业务截图: {screenshot_file_name}')
        
        # 执行断言，如果失败会触发tearDown中的自动截图
        Log.info('开始执行断言')
        self.assertEqual(loginyaml['check'], login_check_hint, f'实际返回结果：{login_check_hint}')
        Log.info(f'✓ 验证通过, 实际返回结果：{login_check_hint}')
        
        if screenshot_name != 'login_locked':
            lp.user_logout()
        sleep(2)


if __name__ == '__main__':
    unittest.main()
