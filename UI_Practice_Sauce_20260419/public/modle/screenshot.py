import inspect
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import setting


def get_testname():
    frame = inspect.currentframe()
    while frame:
        filename = frame.f_code.co_filename
        if 'test_' in filename or 'Test' in filename:
            return Path(filename).stem
        frame = frame.f_back


def insert_img(driver, file_name):
    test_name = get_testname()
    testcase_screenshot_dir = os.path.join(setting.REPORT, 'screenshot', test_name)
    if not os.path.exists(testcase_screenshot_dir):
        os.makedirs(testcase_screenshot_dir)
    file_path = os.path.join(testcase_screenshot_dir, file_name)
    return driver.get_screenshot_as_file(file_path)
