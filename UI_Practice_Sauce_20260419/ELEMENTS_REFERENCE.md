# 元素定位器配置总览

## 📋 配置文件清单

| 页面 | YAML 文件 | 说明 |
|------|----------|------|
| 登录页面 | `testyaml/login.yaml` | 登录、登出相关元素 |
| 商品页面 | `testyaml/product.yaml` | 商品列表、添加/移除购物车元素 |
| 购物车页面 | `testyaml/cart.yaml` | 购物车商品、结算相关元素 |

---

## 🔑 测试账号

- **用户名**: standard_user
- **密码**: secret_sauce

---

## 📍 商品页面元素 (product.yaml)

### 添加商品按钮 (testcase 索引 0-5)

| 索引 | 商品名称 | element_info | 说明 |
|------|---------|--------------|------|
| 0 | Backpack | add-to-cart-sauce-labs-backpack | 添加背包到购物车 |
| 1 | Bike Light | add-to-cart-sauce-labs-bike-light | 添加自行车灯到购物车 |
| 2 | Bolt T-Shirt | add-to-cart-sauce-labs-bolt-t-shirt | 添加Bolt T恤到购物车 |
| 3 | Fleece Jacket | add-to-cart-sauce-labs-fleece-jacket | 添加抓绒夹克到购物车 |
| 4 | Onesie | add-to-cart-sauce-labs-onesie | 添加婴儿连体衣到购物车 |
| 5 | Red T-Shirt | add-to-cart-test.allthethings()-t-shirt-(red) | 添加红色T恤到购物车 |

### 移除商品按钮 (testcase 索引 6-11)

| 索引 | 商品名称 | element_info | 说明 |
|------|---------|--------------|------|
| 6 | Backpack | remove-sauce-labs-backpack | 从购物车移除背包 |
| 7 | Bike Light | remove-sauce-labs-bike-light | 从购物车移除自行车灯 |
| 8 | Bolt T-Shirt | remove-sauce-labs-bolt-t-shirt | 从购物车移除Bolt T恤 |
| 9 | Fleece Jacket | remove-sauce-labs-fleece-jacket | 从购物车移除抓绒夹克 |
| 10 | Onesie | remove-sauce-labs-onesie | 从购物车移除婴儿连体衣 |
| 11 | Red T-Shirt | remove-test.allthethings()-t-shirt-(red) | 从购物车移除红色T恤 |

### 其他操作元素 (testcase 索引 12)

| 索引 | element_info | find_type | 说明 |
|------|--------------|-----------|------|
| 12 | shopping_cart_link | class_name | 点击购物车图标 |

### 验证元素 (check 索引 0-1)

| 索引 | element_info | find_type | operate_type | 说明 |
|------|--------------|-----------|--------------|------|
| 0 | title | class_name | text | 获取页面标题 |
| 1 | inventory_item | class_name | elements | 获取所有商品元素 |

---

## 🛒 购物车页面元素 (cart.yaml)

### 操作元素 (testcase 索引 0-2)

| 索引 | element_info | find_type | operate_type | 说明 |
|------|--------------|-----------|--------------|------|
| 0 | continue-shopping | id | click | 点击继续购物按钮 |
| 1 | checkout | id | click | 点击结算按钮 |
| 2 | cart_button | class_name | click | 点击移除商品按钮 |

### 验证元素 (check 索引 0-5)

| 索引 | element_info | find_type | operate_type | 说明 |
|------|--------------|-----------|--------------|------|
| 0 | title | class_name | text | 获取页面标题 |
| 1 | cart_item | class_name | elements | 获取所有购物车商品项 |
| 2 | cart_quantity | class_name | text | 获取商品数量 |
| 3 | cart_desc_label | class_name | text | 获取商品描述 |
| 4 | inventory_item_price | class_name | text | 获取商品价格 |
| 5 | //div[@class='cart_footer']... | xpath | text | 获取空购物车提示 |

---

## 🔐 登录页面元素 (login.yaml)

### 操作元素 (testcase 索引 0-4)

| 索引 | element_info | find_type | operate_type | 说明 |
|------|--------------|-----------|--------------|------|
| 0 | user-name | id | send_keys | 输入账号 |
| 1 | password | id | send_keys | 输入密码 |
| 2 | submit-button | class_name | click | 点击登录按钮 |
| 3 | react-burger-menu-btn | id | click | 点击菜单弹框 |
| 4 | logout_sidebar_link | id | click | 退出登录 |

### 验证元素 (check 索引 0-1)

| 索引 | element_info | find_type | operate_type | 说明 |
|------|--------------|-----------|--------------|------|
| 0 | app_logo | class_name | text | 获取首页文案 |
| 1 | //h3[@data-test='error'] | xpath | text | 锁定用户提示 |

---

## 💻 代码使用示例

### 在页面对象中使用 YAML 配置

```python
from public.modle.getyaml import GetYaml
from config import setting
from selenium.webdriver.common.by import By

# 加载YAML配置
test_yaml_path = os.path.join(setting.TEST_YAML, 'product.yaml')
testyaml = GetYaml(test_yaml_path)

class ProductPage(BasePage):
    # 从YAML加载元素定位器（通过索引）
    _backpack_add_btn = (By.ID, testyaml.get_element_info(0))
    _cart_link = (By.CLASS_NAME, testyaml.get_element_info(12))
    _page_title = (By.CLASS_NAME, testyaml.get_check_element_info(0))
    
    def add_backpack_to_cart(self):
        """添加背包到购物车"""
        self.find_element(*self._backpack_add_btn).click()
```

### 修改元素定位器

只需修改 YAML 文件，无需改动 Python 代码：

```yaml
# product.yaml - 修改前
testcase:
  -
    element_info: 'add-to-cart-sauce-labs-backpack'
    find_type: id

# product.yaml - 修改后（例如改用 CSS Selector）
testcase:
  -
    element_info: '#add-to-cart-sauce-labs-backpack'
    find_type: css_selector
```

---

## 🎯 维护指南

### 添加新元素

1. 在对应的 YAML 文件中添加新配置项
2. 记录元素的索引位置
3. 在页面对象类中使用该索引

```yaml
# 在 product.yaml 中添加新元素
testcase:
  # ... 现有元素 ...
  -
    element_info: 'new-element-id'
    find_type: id
    operate_type: click
    info: 新元素说明
```

```python
# 在 ProductPage.py 中使用
_new_element = (By.ID, testyaml.get_element_info(13))  # 使用新的索引
```

### 元素变更流程

1. **定位器变化** → 修改 YAML 文件中的 `element_info` 或 `find_type`
2. **新增元素** → 在 YAML 文件末尾添加新配置
3. **删除元素** → 从 YAML 文件中删除对应配置（注意调整后续索引）

### 注意事项

⚠️ **重要**：
- 修改 YAML 文件中的元素顺序会影响索引
- 删除中间的元素会导致后续索引全部变化
- 建议在 YAML 文件中使用注释标记每个元素的用途
- 定期检查和更新过时的元素定位器

---

## 📊 元素统计

| 页面 | testcase 元素数量 | check 元素数量 | 总计 |
|------|------------------|----------------|------|
| 登录页面 | 5 | 2 | 7 |
| 商品页面 | 13 | 2 | 15 |
| 购物车页面 | 3 | 6 | 9 |
| **合计** | **21** | **10** | **31** |

---

## 🔗 相关文档

- [README.md](README.md) - 项目总体说明
- [TEST_CASES.md](TEST_CASES.md) - 测试用例清单
- [YAML_CONFIG_GUIDE.md](YAML_CONFIG_GUIDE.md) - YAML 配置详细指南
