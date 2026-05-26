# YAML 元素配置说明

## 概述
本框架使用 YAML 文件管理页面元素定位器，实现元素与代码分离，便于维护和管理。

## 配置文件位置
所有 YAML 配置文件位于 `testyaml/` 目录下：
- `login.yaml` - 登录页面元素配置
- `product.yaml` - 商品页面元素配置
- `cart.yaml` - 购物车页面元素配置

## YAML 文件结构

每个 YAML 文件包含两个主要部分：

### 1. testcase（操作类元素）
用于用户交互的元素，如按钮、输入框等。

```yaml
testcase:
  -
    element_info: 'user-name'        # 元素定位值
    find_type: id                    # 定位方式
    operate_type: send_keys          # 操作类型
    info: 输入账号                   # 元素说明
```

### 2. check（验证类元素）
用于断言和验证的元素，如文本、列表等。

```yaml
check:
  - 
    element_info: 'app_logo'         # 元素定位值
    find_type: class_name            # 定位方式
    operate_type: text               # 获取类型
    info: 获取首页文案               # 元素说明
```

## 字段说明

### testcase 部分字段

| 字段 | 说明 | 可选值 |
|------|------|--------|
| element_info | 元素定位器的值 | 根据 find_type 而定 |
| find_type | 定位方式 | id, class_name, xpath, css_selector, name, tag_name, link_text, partial_link_text |
| operate_type | 操作类型 | send_keys, click, clear, submit |
| info | 元素描述 | 任意文本 |

### check 部分字段

| 字段 | 说明 | 可选值 |
|------|------|--------|
| element_info | 元素定位器的值 | 根据 find_type 而定 |
| find_type | 定位方式 | id, class_name, xpath, css_selector, name, tag_name, link_text, partial_link_text |
| operate_type | 获取类型 | text, attribute, elements |
| info | 元素描述 | 任意文本 |

## 在代码中使用

### 1. 加载 YAML 配置

```python
from public.modle.getyaml import GetYaml
from config import setting
import os

# 加载商品页面YAML配置
test_yaml_path = os.path.join(setting.TEST_YAML, 'product.yaml')
testyaml = GetYaml(test_yaml_path)
```

### 2. 获取 testcase 元素

```python
# 获取第0个元素的定位信息
element_value = testyaml.get_element_info(0)  # 返回: 'add-to-cart-sauce-labs-backpack'
find_type = testyaml.get_find_type(0)         # 返回: 'id'
operate_type = testyaml.get_operate_type(0)   # 返回: 'click'
info = testyaml.get_info(0)                   # 返回: '添加背包到购物车'

# 在页面对象中使用
from selenium.webdriver.common.by import By
_product_button = (By.ID, testyaml.get_element_info(0))
```

### 3. 获取 check 元素

```python
# 获取第0个验证元素的定位信息
element_value = testyaml.get_check_element_info(0)  # 返回: 'title'
find_type = testyaml.get_check_find_type(0)         # 返回: 'class_name'
operate_type = testyaml.get_check_operate_type(0)   # 返回: 'text'
info = testyaml.get_check_info(0)                   # 返回: '获取页面标题'

# 在页面对象中使用
_page_title = (By.CLASS_NAME, testyaml.get_check_element_info(0))
```

## 完整示例

### product.yaml 配置

```yaml
testcase:
  -
    element_info: 'add-to-cart-sauce-labs-backpack'
    find_type: id
    operate_type: click
    info: 添加背包到购物车
  -
    element_info: 'shopping_cart_link'
    find_type: class_name
    operate_type: click
    info: 点击购物车图标

check:
  -
    element_info: 'title'
    find_type: class_name
    operate_type: text
    info: 获取页面标题
  -
    element_info: 'inventory_item'
    find_type: class_name
    operate_type: elements
    info: 获取所有商品元素
```

### ProductPage.py 使用

```python
from public.modle.getyaml import GetYaml
from config import setting
from selenium.webdriver.common.by import By

# 加载配置
test_yaml_path = os.path.join(setting.TEST_YAML, 'product.yaml')
testyaml = GetYaml(test_yaml_path)

class ProductPage(BasePage):
    # 从YAML加载元素定位器
    _backpack_add_btn = (By.ID, testyaml.get_element_info(0))
    _cart_link = (By.CLASS_NAME, testyaml.get_element_info(1))
    _page_title = (By.CLASS_NAME, testyaml.get_check_element_info(0))
    _inventory_items = (By.CLASS_NAME, testyaml.get_check_element_info(1))
    
    def add_backpack_to_cart(self):
        """添加背包到购物车"""
        self.find_element(*self._backpack_add_btn).click()
    
    def get_page_title(self):
        """获取页面标题"""
        return self.find_element(*self._page_title).text
    
    def get_product_count(self):
        """获取商品数量"""
        products = self.find_elements(*self._inventory_items)
        return len(products)
```

## 最佳实践

### 1. 元素索引管理
- 按照功能模块分组排列元素
- 在 YAML 文件中添加注释说明每个元素的用途
- 保持索引顺序稳定，避免频繁调整

### 2. 命名规范
- element_info 使用语义化的名称
- info 字段用中文清晰描述元素用途
- 相同功能的元素放在一起

### 3. 维护建议
- 页面元素变更时，只修改对应的 YAML 文件
- 定期检查和更新过时的元素定位器
- 为新页面创建独立的 YAML 配置文件

### 4. 定位方式选择优先级
1. **id** - 唯一且稳定，优先使用
2. **name** - 表单元素常用
3. **class_name** - 注意可能有多个元素
4. **css_selector** - 灵活且性能好
5. **xpath** - 功能强大但性能较差，最后考虑

## 注意事项

1. **索引从0开始** - 第一个元素的索引是 0
2. **testcase 和 check 独立计数** - 两部分元素的索引互不影响
3. **YAML 格式严格** - 注意缩进和空格，建议使用 2 空格缩进
4. **特殊字符转义** - XPath 中的引号需要正确转义
5. **编码格式** - YAML 文件必须使用 UTF-8 编码

## 常见问题

### Q: 如何添加新元素？
A: 在对应的 YAML 文件中添加新的配置项，注意保持正确的缩进和格式。

### Q: 元素索引变了怎么办？
A: 更新页面对象类中对应的索引值，或者重新组织 YAML 文件中的元素顺序。

### Q: 支持哪些定位方式？
A: 支持 Selenium 的所有定位方式：id, class_name, xpath, css_selector, name, tag_name, link_text, partial_link_text

### Q: 如何在多个页面共享元素？
A: 可以创建公共的 YAML 文件，或者在多个页面 YAML 中重复定义相同的元素。
