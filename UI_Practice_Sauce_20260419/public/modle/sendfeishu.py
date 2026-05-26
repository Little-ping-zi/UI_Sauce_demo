import configparser
import json
from pathlib import Path
import requests
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import setting
from public.modle import report
from public.modle.log import Log

report_dir = setting.REPORT

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import setting
from requests_toolbelt import MultipartEncoder


class FeishuFileBot:
    def __init__(self):
        # self.app_id = app_id
        # self.app_secret = app_secret
        self.tenant_access_token = None

        con = configparser.ConfigParser()
        con.read(setting.CONFIG, encoding='utf-8')
        self.app_id = con.get('FEISHU_APP', 'APP_ID')
        self.app_secret = con.get('FEISHU_APP', 'APP_SECRET')
        self.receive_id = con.get('FEISHU_APP', 'CHAT_ID')
        self.receive_id_type = 'chat_id'

    def get_token(self):
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
            'app_id': self.app_id,
            'app_secret': self.app_secret
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get('code') == 0:
            self.tenant_access_token = result.get('tenant_access_token')
        else:
            Log.error('获取tenant_access_token失败')
            return False

    def upload_file(self, file_path):
        if not self.tenant_access_token:
            self.get_token()

        url = 'https://open.feishu.cn/open-apis/im/v1/files'

        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            form = {
                'file_type': 'stream',
                'file_name': file_name,
                'file': (file_name, f, 'text/html')
            }
            multi_form = MultipartEncoder(form)
            headers = {
                'Authorization': f'Bearer {self.tenant_access_token}',
                'Content-Type': multi_form.content_type
            }

            response = requests.post(url, headers=headers, data=multi_form)
        result = response.json()

        if result.get('code') == 0:
            file_key = result.get('data').get('file_key')
            return file_key
        else:
            Log.error('文件上传失败')
            return None

    def send_message_to_chat(self, stats):
        url = f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'

        self.get_token()

        headers = {
            'Authorization': f'Bearer {self.tenant_access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }

        msgContent = {
            "type": "template",
            "data":
                {
                    "template_id": "AAqeXzYioIsqo",
                    "template_version_name": "1.0.1",
                    "template_variable":
                        {
                            "tester": stats['tester'],
                            "start_time": stats['start_time'],
                            "duration": stats['duration'],
                            "total": stats['total'],
                            "passed": stats['passed'],
                            "failed": stats['failed'],
                            "pass_rate": stats['pass_rate']
                        }
                }
        }

        data = {
                "receive_id": self.receive_id,
                "msg_type": "interactive",
                "content": json.dumps(msgContent)
        }
        payload = json.dumps(data)

        response = requests.post(url, headers=headers, data=payload)

        return response.json()

    def send_file_to_chat(self, file_key):
        url = f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={self.receive_id_type}'
        headers = {
            'Authorization': f'Bearer {self.tenant_access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }

        data = {
            'receive_id': self.receive_id,
            'msg_type': 'file',
            'content': json.dumps({"file_key": file_key})
        }
        response = requests.post(url, headers=headers, json=data)

        return response.json()