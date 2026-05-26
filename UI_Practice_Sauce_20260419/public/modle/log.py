import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import setting


class Log:
    _instance = None
    _log_file = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()

        return cls._instance

    def _init_logger(self):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        log_name = f'test_run{timestamp}.log'
        self._log_file = os.path.join(setting.LOG, log_name)

        self._logger = logging.getLogger('AutoTest')
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.handlers:
            file_handle = logging.FileHandler(self._log_file, encoding='utf-8')
            file_handle.setLevel(logging.DEBUG)

            console_handle = logging.StreamHandler()
            console_handle.setLevel(logging.DEBUG)

            format = logging.Formatter(
                '[%(asctime)s] [%(filename)s|%(funcName)s] [line:%(lineno)d] %(levelname)-8s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            file_handle.setFormatter(format)
            console_handle.setFormatter(format)

            self._logger.addHandler(file_handle)
            self._logger.addHandler(console_handle)

            self._logger.info('=' * 80)
            self._logger.info(f'测试运行开始时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            self._logger.info(f'日志文件：{self._log_file}')
            self._logger.info('=' * 80)

    @classmethod
    def get_log_file(cls):
        if cls._instance is None:
            cls._instance = Log()
        return cls._log_file

    @classmethod
    def debug(cls, message):
        if cls._instance is None:
            cls._instance = Log()
        cls._instance._logger.debug(message, stacklevel=2)

    @classmethod
    def info(cls, message):
        if cls._instance is None:
            cls._instance = Log()
        cls._instance._logger.info(message, stacklevel=2)

    @classmethod
    def warning(cls, message):
        if cls._instance is None:
            cls._instance = Log()
        cls._instance._logger.warning(message, stacklevel=2)

    @classmethod
    def error(cls, message):
        if cls._instance is None:
            cls._instance = Log()
        cls._instance._logger.error(message, stacklevel=2)