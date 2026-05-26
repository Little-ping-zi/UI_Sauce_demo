import sys


# 分流输出：控制台 + 文件 同时打印
class DualOutput:
    def __init__(self, file_path):
        self.file = open(file_path, "w", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, data):
        self.stdout.write(data)  # 打印到控制台
        self.file.write(data)  # 写入文件
        self.flush()

    def flush(self):
        self.stdout.flush()
        self.file.flush()
