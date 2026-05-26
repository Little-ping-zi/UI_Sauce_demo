# 导入路径处理模块，用于跨平台的路径操作
from pathlib import Path
# 导入Chrome驱动管理器，自动下载和管理ChromeDriver版本
from webdriver_manager.chrome import ChromeDriverManager
# 导入Chrome服务类，用于配置浏览器启动参数
from selenium.webdriver.chrome.service import Service
# 导入Selenium核心模块，用于Web自动化测试
from selenium import webdriver
# 导入单元测试框架
import unittest
# 导入系统模块，用于修改Python模块搜索路径
import sys
# 将项目根目录添加到模块搜索路径的开头，确保能正确导入public包
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
# 导入自定义日志模块，用于记录测试执行过程
from public.modle.log import Log
# 导入截图工具函数，用于测试失败时保存现场
from public.modle.screenshot import insert_img
# 导入时间模块，用于添加等待和生成唯一文件名
import time

class MyTest(unittest.TestCase):
    """
    自定义测试基类，继承自unittest.TestCase
    所有测试类都应继承此类以复用浏览器初始化和清理逻辑
    """

    @classmethod
    def setUpClass(cls):
        """
        类级别的初始化方法，在整个测试类开始执行前运行一次
        负责创建浏览器实例并进行基础配置
        """
        # 记录分隔线，便于区分不同测试类的执行
        Log.info('=' * 80)
        # 记录当前开始执行的测试类名称
        Log.info(f'开始执行测试类：{cls.__name__}')
        try:
            # 使用ChromeDriverManager自动下载并安装匹配的ChromeDriver
            # 避免手动管理驱动版本的麻烦
            service = Service(ChromeDriverManager().install())
            # 创建Chrome浏览器实例，传入配置好的服务
            cls.driver = webdriver.Chrome(service=service)
            # 设置隐式等待时间为10秒，全局生效于所有元素查找操作
            cls.driver.implicitly_wait(10)
            # 最大化浏览器窗口，确保页面元素完整显示
            cls.driver.maximize_window()
        except Exception as e:
            # 如果浏览器启动失败，记录错误日志
            Log.error('浏览器启动失败')

    @classmethod
    def tearDownClass(cls):
        """
        类级别的清理方法，在整个测试类执行结束后运行一次
        负责关闭浏览器并释放资源
        """
        # 记录测试类执行结束
        Log.info(f'结束执行测试类：{cls.__name__}')
        # 记录分隔线
        Log.info('-'*80)
        # 关闭浏览器并退出WebDriver会话
        cls.driver.quit()

    def setUp(self):
        """
        方法级别的初始化，在每个测试方法执行前都会运行
        用于确保测试环境干净、浏览器状态正常
        """
        # 记录当前正在执行的测试方法名称
        Log.info(f'▶ 开始测试：{self._testMethodName}')
        
        try:
            # 检查浏览器是否仍然可用（防止意外关闭）
            if not hasattr(self, 'driver') or self.driver is None:
                Log.error('浏览器实例不存在，尝试重新创建')
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service)
                self.driver.implicitly_wait(10)
                self.driver.maximize_window()
            
            # 验证浏览器会话是否有效
            self.driver.title
            Log.debug('浏览器状态正常')
            
        except Exception as e:
            # 如果浏览器不可用，记录错误并重新创建
            Log.error(f'浏览器状态异常: {str(e)}，重新创建浏览器实例')
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service)
                self.driver.implicitly_wait(10)
                self.driver.maximize_window()
            except Exception as retry_error:
                Log.error(f'重新创建浏览器失败: {str(retry_error)}')
                raise

    def tearDown(self):
        """
        方法级别的清理，在每个测试方法执行后都会运行
        包含失败截图、测试结果记录等功能
        """
        # 获取当前测试方法的真实执行结果
        is_failed = False
        
        # Python 3.9+ 使用 _outcome 检测失败
        if hasattr(self, '_outcome'):
            # 检查是否有错误或失败
            if hasattr(self._outcome, 'errors') and self._outcome.errors:
                # 遍历所有错误，检查是否是真正的断言失败或异常
                for test, traceback in self._outcome.errors:
                    if traceback is not None:  # 只有当有实际的错误信息时才标记为失败
                        is_failed = True
                        break
        
        # 如果测试出现错误或失败，自动截图保存现场
        if is_failed:
            try:
                # 生成带时间戳的唯一文件名
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                screenshot_name = f'{self._testMethodName}_fail_{timestamp}.png'
                
                # 调用截图函数保存图片
                insert_img(self.driver, screenshot_name)
                Log.warning(f'⚠ 测试失败，已自动保存截图: {screenshot_name}')
            except Exception as e:
                Log.error(f'截图失败: {str(e)}')
        
        # 清除浏览器cookies，为下一个测试提供干净的环境
        try:
            self.driver.delete_all_cookies()
            Log.debug('已清除浏览器Cookies')
        except Exception as e:
            Log.warning(f'清除Cookies失败: {str(e)}')
        
        # 记录测试方法执行完成
        status = '❌ 失败' if is_failed else '✅ 通过'
        Log.info(f'{status} 结束测试：{self._testMethodName}')
        Log.info('-' * 60)