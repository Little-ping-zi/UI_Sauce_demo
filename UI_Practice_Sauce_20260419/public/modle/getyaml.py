import yaml
from selenium.webdriver.common.by import By


class GetYaml:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path
        self._data = None

    def _load(self):
        """加载YAML文件"""
        if self._data is None:
            with open(self.yaml_path, encoding='utf-8') as f:
                self._data = yaml.safe_load(f)
        return self._data

    # ========== 旧版方法（保持兼容性）==========
    
    def get_testcase(self, i):
        """获取testcase部分的第i个元素（旧版）"""
        data = self._load()
        return data.get('testcase', [])[i]

    def get_element_info(self, i):
        """获取testcase元素的定位值（旧版）"""
        return self.get_testcase(i)['element_info']

    def get_find_type(self, i):
        """获取testcase元素的定位类型（旧版）"""
        return self.get_testcase(i)['find_type']

    def get_operate_type(self, i):
        """获取testcase元素的操作类型（旧版）"""
        return self.get_testcase(i)['operate_type']

    def get_info(self, i):
        """获取testcase元素的描述（旧版）"""
        return self.get_testcase(i)['info']

    def get_check(self, i):
        """获取check部分的第i个元素（旧版）"""
        data = self._load()
        return data.get('check', [])[i]

    def get_check_element_info(self, i):
        """获取check元素的定位值（旧版）"""
        return self.get_check(i)['element_info']

    def get_check_find_type(self, i):
        """获取check元素的定位类型（旧版）"""
        return self.get_check(i)['find_type']

    def get_check_operate_type(self, i):
        """获取check元素的操作类型（旧版）"""
        return self.get_check(i)['operate_type']

    def get_check_info(self, i):
        """获取check元素的描述（旧版）"""
        return self.get_check(i)['info']

    # ========== 新版方法（键名映射方式）==========
    
    def get_element(self, element_name):
        """
        根据键名获取元素配置（新版）
        :param element_name: 元素键名，如 'backpack_add'
        :return: 元素配置字典 {'locator': '...', 'type': '...', 'description': '...'}
        """
        data = self._load()
        elements = data.get('elements', {})
        if element_name not in elements:
            raise KeyError(f"Element '{element_name}' not found in {self.yaml_path}")
        return elements[element_name]
    
    def get_locator(self, element_name):
        """
        根据键名获取元素定位值（新版）
        :param element_name: 元素键名
        :return: 定位值字符串
        """
        return self.get_element(element_name)['locator']
    
    def get_type(self, element_name):
        """
        根据键名获取元素定位类型（新版）
        :param element_name: 元素键名
        :return: 定位类型字符串 (id, class_name, xpath, etc.)
        """
        return self.get_element(element_name)['type']
    
    def get_description(self, element_name):
        """
        根据键名获取元素描述（新版）
        :param element_name: 元素键名
        :return: 描述字符串
        """
        return self.get_element(element_name)['description']
    
    def get_by_locator(self, element_name):
        """
        根据键名获取Selenium的By定位器元组（新版）
        :param element_name: 元素键名
        :return: (By type, locator) 元组
        """
        element_config = self.get_element(element_name)
        locator = element_config['locator']
        loc_type = element_config['type'].upper()
        
        # 将字符串转换为By类的属性
        by_type = getattr(By, loc_type)
        return (by_type, locator)
    
    def get_all_elements(self):
        """
        获取所有元素配置（新版）
        :return: 元素字典 {name: {locator, type, description}}
        """
        data = self._load()
        return data.get('elements', {})


