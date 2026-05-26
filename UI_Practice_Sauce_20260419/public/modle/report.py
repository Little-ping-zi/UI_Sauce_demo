import re
import time, sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import setting
from package.HTMLTestRunner import HTMLTestRunner


def creat_report(testcase):
    """
    生成HTML测试报告，同时在控制台输出测试结果
    """
    import sys
    
    strftime = time.strftime('%Y%m%d_%H%M%S')
    report_name = os.path.join(setting.REPORT, f'{strftime}_result.html')
    
    # 创建 HTML 报告
    with open(report_name, 'wb') as f:
        runner = HTMLTestRunner(
            stream=f,
            title='UI自动化测试报告',
            description='Chrome',
            tester='Zoe',
            verbosity=2  # 设置详细程度
        )
        result = runner.run(testcase)
    
    # 在控制台输出总结信息
    print('\n' + '='*80)
    print('测试执行完成！')
    print('='*80)
    print(f'总用例数: {result.testsRun}')
    print(f'通过: {result.testsRun - len(result.failures) - len(result.errors)}')
    print(f'失败: {len(result.failures)}')
    print(f'错误: {len(result.errors)}')
    print(f'报告路径: {report_name}')
    print('='*80)
    
    # 如果有失败或错误，在控制台输出详细信息
    if result.failures or result.errors:
        print('\n❌ 失败的测试用例:')
        print('-' * 80)
        for test, traceback in result.failures:
            print(f'\n【失败】{test}')
            print(traceback)
        
        for test, traceback in result.errors:
            print(f'\n【错误】{test}')
            print(traceback)


def new_report(report_dir):
    report_list = os.listdir(report_dir)
    report_list.sort(key=lambda f: os.path.getmtime(os.path.join(report_dir, f)))
    return os.path.join(report_dir, report_list[-1])


def parse_report(file_path):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()

    stats = {}
    match = re.search('<strong>测试人员:</strong>\s*(.+?)\s*<', content)
    stats['tester'] = match.group(1) if match else 'Unknown'

    match = re.search('<strong>开始时间:</strong>\s*(.+?)\s*<', content)
    stats['start_time'] = match.group(1) if match else ''

    match = re.search('<strong>合计耗时:</strong>\s*(.+?)\s*<', content)
    stats['duration'] = match.group(1) if match else ''

    # 通用解析测试结果，适配多种格式：
    # 格式1: 总共 15 通过 4 失败 3 错误 8 通过率 = 26.67%
    # 格式2: 总共 20 通过 20 通过率 = 100.00%
    # 格式3: 总共 10, 通过 8, 失败 2, 通过率 = 80.00%
    # 格式4: Total: 15, Pass: 4, Fail: 3, Error: 8, Pass Rate: 26.67%
    
    # 提取总数
    match_total = re.search(r'总共[:\s]*(\d+)', content)
    stats['total'] = int(match_total.group(1)) if match_total else 0
    
    # 提取通过数
    match_passed = re.search(r'通过[:\s]*(\d+)', content)
    stats['passed'] = int(match_passed.group(1)) if match_passed else 0
    
    # 提取失败数（包括 Fail 和 Error）
    match_failed = re.search(r'失败[:\s]*(\d+)', content)
    failed_count = int(match_failed.group(1)) if match_failed else 0
    
    match_error = re.search(r'错误[:\s]*(\d+)', content)
    error_count = int(match_error.group(1)) if match_error else 0
    
    stats['failed'] = failed_count + error_count  # 合并失败和错误
    
    # 提取通过率
    match_rate = re.search(r'通过率[:\s]*=\s*([\d.]+%)', content)
    stats['pass_rate'] = match_rate.group(1) if match_rate else '0.00%'

    return stats

if __name__=='__main__':
    latest_report = new_report(setting.REPORT)
    result = parse_report(latest_report)
    print(result)
