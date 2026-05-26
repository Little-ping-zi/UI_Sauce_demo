import unittest

from testcase.test_cart import TestCart
from testcase.test_login import TestLogin
from testcase.test_product import TestProduct
from public.modle import report
from config import setting
from public.modle.sendfeishu import FeishuFileBot
from public.modle.log import Log

report_dir = setting.REPORT


def run_all_tests():
    """
    运行所有测试用例
    包括登录、商品和购物车测试
    """
    suite = unittest.TestSuite()

    # 添加登录测试
    suite.addTest(unittest.makeSuite(TestLogin))
    
    # 添加商品测试
    suite.addTest(unittest.makeSuite(TestProduct))
    
    # 添加购物车测试
    suite.addTest(unittest.makeSuite(TestCart))

    return suite


def run_main_flow_tests():
    """
    只运行主流程测试用例
    标记为@unittest.skip的主流程测试需要手动取消skip来运行
    """
    suite = unittest.TestSuite()

    # 添加登录测试（主流程）
    suite.addTest(unittest.makeSuite(TestLogin))
    
    # 添加商品主流程测试
    # 注意：需要在测试方法中取消@unittest.skip装饰器来运行
    suite.addTest(unittest.makeSuite(TestProduct))
    
    # 添加购物车主流程测试
    suite.addTest(unittest.makeSuite(TestCart))

    return suite


def send_report_to_feishu(report_path):
    bot = FeishuFileBot()
    file_key = bot.upload_file(report_path)
    result = bot.send_file_to_chat(file_key)
    if result.get('code') == 0:
        Log.info('测试报告发送成功')
    else:
        Log.error('测试报告发送失败')


def send_card_message_to_feishu(stats):
    bot = FeishuFileBot()
    messageResult = bot.send_message_to_chat(stats)
    Log.debug(messageResult)

    if messageResult.get('code') == 0:
        Log.info('卡片信息发送成功')
    else:
        Log.error('卡片信息发送失败')


if __name__ == '__main__':
    # 运行所有测试用例
    suite = run_all_tests()
    
    # 生成测试报告
    report.creat_report(suite)
    
    # 获取最新报告并发送（可选）
    latest_report = report.new_report(report_dir)
    stats = report.parse_report(latest_report)

    # 发送卡片消息到飞书群
    send_card_message_to_feishu(stats)

    # 发送报告文件到飞书群
    send_report_to_feishu(latest_report)
