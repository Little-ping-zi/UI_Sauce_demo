# Sauce Demo UI自动化测试框架

## 项目概述
本项目是基于Selenium的UI自动化测试框架，针对Sauce Demo网站进行测试。

## 测试账号
- **用户名**: standard_user
- **密码**: secret_sauce

## 测试页面
- **商品详情页**: https://www.saucedemo.com/inventory.html
- **购物车页面**: https://www.saucedemo.com/cart.html

## 项目结构
```
UI_Practice_Sauce_20260419/
├── config/                 # 配置文件
│   ├── base.ini           # 基础配置（URL等）
│   └── setting.py         # 路径配置
├── public/                # 公共模块
│   ├── modle/            # 工具模块
│   │   ├── myunit.py     # 测试基类
│   │   ├── log.py        # 日志模块
│   │   ├── screenshot.py # 截图模块
│   │   ├── getyaml.py    # YAML解析模块
│   │   └── ...
│   └── pageobjects/      # 页面对象
│       ├── base_page.py  # 页面基类
│       ├── login_page.py # 登录页面
│       ├── product_page.py # 商品页面
│       └── cart_page.py  # 购物车页面
├── testcase/             # 测试用例
│   ├── test_login.py     # 登录测试
│   ├── test_product.py   # 商品测试
│   └── test_cart.py      # 购物车测试
├── testdata/             # 测试数据
├── testyaml/             # YAML元素配置
│   ├── login.yaml        # 登录页面元素
│   ├── product.yaml      # 商品页面元素
│   └── cart.yaml         # 购物车页面元素
├── report/               # 测试报告
│   └── screenshot/       # 截图文件
├── log/                  # 日志文件
└── run.py               # 测试执行入口
```

## 测试用例说明

### 1. 商品详情页测试 (test_product.py)

#### 主流程测试用例（标识为 【主流程】）
- ✅ `test_product_page_loads_successfully` - 验证商品页面正常加载
- ✅ `test_add_single_product_to_cart` - 验证添加单个商品到购物车
- ✅ `test_add_multiple_products_to_cart` - 验证添加多个商品到购物车

#### 边界场景测试用例
- `test_remove_product_from_cart` - 验证从购物车移除商品
- `test_navigate_to_cart_from_product_page` - 验证从商品页跳转到购物车
- `test_all_products_are_displayed` - 验证所有商品正确显示
- `test_product_page_title_verification` - 验证页面标题正确性

### 2. 购物车页面测试 (test_cart.py)

#### 主流程测试用例（标识为 【主流程】）
- ✅ `test_cart_page_loads_successfully` - 验证购物车页面正常加载
- ✅ `test_cart_items_count_is_correct` - 验证购物车商品数量正确
- ✅ `test_cart_items_information_is_correct` - 验证购物车商品信息正确

#### 边界场景测试用例
- `test_remove_item_from_cart` - 验证从购物车移除商品
- `test_continue_shopping_returns_to_product_page` - 验证继续购物返回商品页
- `test_empty_cart_display` - 验证空购物车显示
- `test_cart_persistence_after_navigation` - 验证购物车内容在导航后保持

## 如何运行测试

### 运行所有测试用例
```bash
python run.py
```
所有测试用例（包括主流程和边界场景）都会执行。

### 识别主流程测试
主流程测试在文档字符串中以 `【主流程】` 标识，方便查看和统计。

### 运行特定测试类
```bash
python -m unittest testcase.test_product.TestProduct
python -m unittest testcase.test_cart.TestCart
```

### 运行特定测试方法
```bash
python -m unittest testcase.test_product.TestProduct.test_add_single_product_to_cart
```

## 主流程测试用例标识

主流程测试用例在文档字符串中以 `【主流程】` 开头标识，例如：
```python
def test_product_page_loads_successfully(self):
    """
    【主流程】验证商品页面能够成功加载
    ...
    """
```

这样做的好处：
1. ✅ 主流程测试会正常执行，不会被跳过
2. ✅ 通过查看文档字符串可以快速识别主流程
3. ✅ 便于生成测试报告时统计主流程覆盖率

## 测试报告
测试报告自动生成在 `report/` 目录下，包含HTML格式的报告和失败时的截图。

## 日志
测试日志保存在 `log/` 目录下，按时间戳命名。

## YAML 元素配置管理

### 配置文件结构
每个页面对应一个 YAML 文件，包含两个部分：
- **testcase**: 操作类元素（按钮、输入框等）
- **check**: 验证类元素（文本、列表等）

### YAML 配置示例
```yaml
testcase:
  -
    element_info: 'user-name'
    find_type: id
    operate_type: send_keys
    info: 输入账号
  -
    element_info: 'submit-button'
    find_type: class_name
    operate_type: click
    info: 点击登录按钮

check:
  - 
    element_info: 'app_logo'
    find_type: class_name
    operate_type: text
    info: 获取首页文案
```

### 在页面对象中使用
```python
from public.modle.getyaml import GetYaml
from config import setting

# 加载YAML配置
test_yaml_path = os.path.join(setting.TEST_YAML, 'product.yaml')
testyaml = GetYaml(test_yaml_path)

# 使用YAML中的元素定位器
_product_button = (By.ID, testyaml.get_element_info(0))
_page_title = (By.CLASS_NAME, testyaml.get_check_element_info(0))
```

### 优势
1. ✅ **元素与代码分离** - 修改元素定位器无需修改代码
2. ✅ **集中管理** - 所有元素定位器在一个文件中
3. ✅ **易于维护** - 清晰的注释和说明
4. ✅ **支持多种定位方式** - id, class_name, xpath, css_selector 等

## 注意事项
1. 确保已安装所需的依赖包
2. Chrome浏览器和ChromeDriver版本需要兼容
3. 测试执行时会自动下载匹配的ChromeDriver
4. 失败的测试会自动截图保存到 `report/screenshot/` 目录
