# 测试用例清单

## 测试环境信息
- **测试网站**: Sauce Demo (https://www.saucedemo.com)
- **测试账号**: standard_user / secret_sauce
- **商品页面**: https://www.saucedemo.com/inventory.html
- **购物车页面**: https://www.saucedemo.com/cart.html

---

## 📌 商品详情页测试用例 (test_product.py)

### ✅ 主流程测试用例（Critical Path）

| 编号 | 测试方法 | 测试目的 | 当前状态 |
|------|---------|---------|---------|
| TC-PROD-001 | `test_product_page_loads_successfully` | 验证商品页面能够成功加载，页面标题正确，商品列表存在 | ✅ Active |
| TC-PROD-002 | `test_add_single_product_to_cart` | 验证单个商品可以成功添加到购物车，添加按钮变为移除按钮 | ✅ Active |
| TC-PROD-003 | `test_add_multiple_products_to_cart` | 验证多个商品可以成功添加到购物车 | ✅ Active |

**主流程标识**：测试方法文档字符串中以 `【主流程】` 开头

### 📋 边界场景测试用例

| 编号 | 测试方法 | 测试目的 | 当前状态 |
|------|---------|---------|---------|
| TC-PROD-004 | `test_remove_product_from_cart` | 验证可以从购物车移除商品，移除按钮变回添加按钮 | ✅ Active |
| TC-PROD-005 | `test_navigate_to_cart_from_product_page` | 验证可以从商品页面跳转到购物车页面 | ✅ Active |
| TC-PROD-006 | `test_all_products_are_displayed` | 验证所有6个商品都正确显示 | ✅ Active |
| TC-PROD-007 | `test_product_page_title_verification` | 验证商品页面标题为'Products' | ✅ Active |

---

## 📌 购物车页面测试用例 (test_cart.py)

### ✅ 主流程测试用例（Critical Path）

| 编号 | 测试方法 | 测试目的 | 当前状态 |
|------|---------|---------|---------|
| TC-CART-001 | `test_cart_page_loads_successfully` | 验证购物车页面能够成功加载，页面标题正确 | ✅ Active |
| TC-CART-002 | `test_cart_items_count_is_correct` | 验证购物车中商品数量与添加的数量一致 | ✅ Active |
| TC-CART-003 | `test_cart_items_information_is_correct` | 验证购物车中商品信息（名称、价格）正确显示 | ✅ Active |

**主流程标识**：测试方法文档字符串中以 `【主流程】` 开头

### 📋 边界场景测试用例

| 编号 | 测试方法 | 测试目的 | 当前状态 |
|------|---------|---------|---------|
| TC-CART-004 | `test_remove_item_from_cart` | 验证可以从购物车移除商品，商品数量减少 | ✅ Active |
| TC-CART-005 | `test_continue_shopping_returns_to_product_page` | 验证点击继续购物按钮返回商品页面 | ✅ Active |
| TC-CART-006 | `test_empty_cart_display` | 验证空购物车的显示和页面标题 | ✅ Active |
| TC-CART-007 | `test_cart_persistence_after_navigation` | 验证购物车内容在页面导航后保持不变 | ✅ Active |

---

## 🔧 测试执行说明

### 运行所有测试用例（包括主流程和边界场景）
```bash
python run.py
```

### 只运行主流程测试用例
使用 pytest 标记或自定义测试选择器（需要额外配置）

或者通过测试方法名过滤：
```bash
# 运行包含特定关键词的测试
python -m unittest discover -s testcase -p "test_*.py" -v | findstr "主流程"
```

### 运行特定测试类
```bash
# 只运行商品测试
python -m unittest testcase.test_product.TestProduct

# 只运行购物车测试
python -m unittest testcase.test_cart.TestCart
```

### 运行特定测试方法
```bash
# 运行单个测试方法
python -m unittest testcase.test_product.TestProduct.test_remove_product_from_cart
```

---

## 📊 测试覆盖范围

### 商品页面功能覆盖
- ✅ 页面加载和显示
- ✅ 商品列表展示
- ✅ 添加商品到购物车
- ✅ 从购物车移除商品
- ✅ 页面导航到购物车
- ✅ 页面标题验证

### 购物车页面功能覆盖
- ✅ 页面加载和显示
- ✅ 商品数量统计
- ✅ 商品信息展示（名称、价格）
- ✅ 移除商品功能
- ✅ 继续购物导航
- ✅ 空购物车处理
- ✅ 数据持久性验证

---

## 📝 测试数据

### 可用商品列表
1. Sauce Labs Backpack (backpack)
2. Sauce Labs Bike Light (bike_light)
3. Sauce Labs Bolt T-Shirt (bolt_shirt)
4. Sauce Labs Fleece Jacket (fleece_jacket)
5. Sauce Labs Onesie (onesie)
6. Test.allTheThings() T-Shirt (Red) (red_tshirt)

---

## ⚠️ 注意事项

1. **主流程测试默认执行**：主流程测试用例会正常执行，在文档字符串中以 `【主流程】` 标识
2. **自动截图**：失败的测试会自动截图保存到 `report/screenshot/` 目录
3. **日志记录**：所有测试执行过程都会记录到 `log/` 目录
4. **浏览器管理**：每个测试类共享一个浏览器实例，测试方法间会清除cookies
5. **隐式等待**：全局设置10秒隐式等待时间

---

## 🎯 测试优先级建议

### P0 - 必须执行（主流程）
- TC-PROD-001, TC-PROD-002, TC-PROD-003
- TC-CART-001, TC-CART-002, TC-CART-003

### P1 - 重要功能
- TC-PROD-004, TC-PROD-005
- TC-CART-004, TC-CART-005

### P2 - 边界场景
- TC-PROD-006, TC-PROD-007
- TC-CART-006, TC-CART-007
