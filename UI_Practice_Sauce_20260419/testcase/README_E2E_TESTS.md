# 业务场景自动化测试指南

## 📋 概述

本目录包含基于 Excel 中 **Sheet2: 业务场景测试用例** 的完整自动化测试实现。

### 测试文件
- **test_e2e_business_scenarios.py**: 端到端业务场景自动化测试（12个用例）

---

## 🎯 测试覆盖

### P0 主流程（4个）- 必须通过
| 用例编号 | 测试方法 | 描述 |
|---------|---------|------|
| TC-E2E-001 | `test_E2E_001_complete_shopping_flow` | 完整购物流程：登录→添加商品→查看购物车 |
| TC-E2E-002 | `test_E2E_002_add_multiple_products` | 多商品添加到购物车 |
| TC-LOGIN-E2E-001 | `test_LOGIN_E2E_001_login_and_logout` | 有效用户登录并登出 |
| TC-E2E-006 | `test_E2E_006_verify_product_page_load` | 登录后验证商品页面加载 |

### P1 重要功能（6个）- 应该通过
| 用例编号 | 测试方法 | 描述 |
|---------|---------|------|
| TC-E2E-003 | `test_E2E_003_remove_product_from_cart` | 从购物车移除商品 |
| TC-E2E-004 | `test_E2E_004_continue_shopping` | 继续购物返回商品页 |
| TC-E2E-007 | `test_E2E_007_add_remove_combination` | 商品添加和移除组合操作 |
| TC-LOGIN-E2E-002 | `test_LOGIN_E2E_002_invalid_password` | 无效密码登录失败 |
| TC-PROD-E2E-001 | `test_PROD_E2E_001_browse_all_products` | 浏览所有商品并验证信息 |
| TC-CART-E2E-001 | `test_CART_E2E_001_verify_prices` | 购物车商品价格验证 |

### P2 一般功能（2个）- 可以通过
| 用例编号 | 测试方法 | 描述 |
|---------|---------|------|
| TC-E2E-005 | `test_E2E_005_empty_cart_state` | 空购物车状态验证 |
| TC-NAV-E2E-001 | `test_NAV_E2E_001_navigation_fluency` | 页面间导航流畅性测试 |

---

## 🚀 执行方式

### 1. 运行所有业务场景测试

```bash
cd UI_Practice_Sauce_20260419
python -m pytest testcase/test_e2e_business_scenarios.py -v
```

### 2. 只运行 P0 主流程测试

```bash
python -m pytest testcase/test_e2e_business_scenarios.py -v -k "E2E_001 or E2E_002 or LOGIN_E2E_001 or E2E_006"
```

### 3. 只运行 P1 重要功能测试

```bash
python -m pytest testcase/test_e2e_business_scenarios.py -v -k "E2E_003 or E2E_004 or E2E_007 or LOGIN_E2E_002 or PROD_E2E_001 or CART_E2E_001"
```

### 4. 运行单个测试用例

```bash
# 完整购物流程
python -m pytest testcase/test_e2e_business_scenarios.py::TestE2EBusinessScenarios::test_E2E_001_complete_shopping_flow -v

# 移除商品
python -m pytest testcase/test_e2e_business_scenarios.py::TestE2EBusinessScenarios::test_E2E_003_remove_product_from_cart -v
```

### 5. 使用 unittest 运行

```bash
cd UI_Practice_Sauce_20260419
python testcase/test_e2e_business_scenarios.py
```

### 6. 生成 HTML 报告

```bash
# 使用 run.py（如果项目中有配置）
python run.py

# 或使用 pytest-html
pip install pytest-html
python -m pytest testcase/test_e2e_business_scenarios.py --html=report/business_scenarios_report.html --self-contained-html
```

---

## 📊 测试特性

### 1. 自动截图
- ✅ 测试失败时自动截图
- 📁 截图保存位置: `report/screenshot/`
- 📝 命名规则: `{测试方法名}_failed.png`

### 2. 详细日志
每个测试用例执行成功后会打印确认信息：
```
✓ TC-E2E-001 执行成功: 完整购物流程验证通过
```

### 3. 完整的断言验证
- 页面标题验证
- URL 验证
- 元素存在性验证
- 数量验证
- 文本内容验证
- 价格格式验证

### 4. 合理的等待时间
- 使用 `sleep()` 确保页面加载完成
- 隐式等待 10 秒
- 关键操作后添加适当延迟

---

## 🔧 前置条件

### 1. 环境要求
```bash
pip install selenium
pip install pytest
```

### 2. ChromeDriver
确保已安装与 Chrome 浏览器版本匹配的 ChromeDriver

### 3. 配置文件
确认 `config/setting.py` 中配置了正确的测试 URL：
```python
TEST_URL = "https://www.saucedemo.com"
```

### 4. 测试账号
- 用户名: `standard_user`
- 密码: `secret_sauce`

---

## 📝 测试用例详解

### TC-E2E-001: 完整购物流程

**测试目的**: 验证核心购物流程的完整性

**关键验证点**:
1. 登录成功跳转到商品页
2. 添加商品后购物车数量为 1
3. 购物车中显示正确的商品名称

**代码示例**:
```python
def test_E2E_001_complete_shopping_flow(self):
    # 登录
    login_page.login("standard_user", "secret_sauce")
    
    # 添加商品
    product_page.add_product_to_cart("backpack")
    
    # 进入购物车
    product_page.go_to_cart()
    
    # 验证
    self.assertEqual(cart_page.get_cart_items_count(), 1)
```

---

### TC-E2E-003: 移除商品

**测试目的**: 验证购物车移除功能的正确性

**关键验证点**:
1. 初始有 2 件商品
2. 移除后剩 1 件商品
3. 购物车数量正确更新

**业务流程**:
```
添加2件商品 → 进入购物车 → 移除1件 → 验证剩余1件
```

---

### TC-E2E-007: 组合操作

**测试目的**: 验证复杂的添加/移除组合场景

**关键验证点**:
1. 每次操作后数量正确
2. 最终包含预期的商品
3. 跨页面操作数据一致性

**业务流程**:
```
添加2件 → 移除1件 → 返回商品页 → 再添加1件 → 验证最终2件
```

---

## 🐛 常见问题

### Q1: 测试执行时报错 "ChromeDriver not found"
**解决方案**:
```bash
# 下载对应版本的 ChromeDriver
# 或安装 webdriver-manager
pip install webdriver-manager
```

### Q2: 元素找不到超时
**解决方案**:
- 增加 `sleep()` 时间
- 检查网络连接
- 确认页面已完全加载

### Q3: 断言失败但页面看起来正常
**解决方案**:
- 检查元素定位器是否正确
- 查看失败截图分析问题
- 验证页面实际内容与预期是否一致

### Q4: 如何调试单个测试用例？
**解决方案**:
```python
# 在测试方法中添加断点
import pdb; pdb.set_trace()

# 或使用 IDE 的调试功能
```

---

## 📈 测试结果分析

### 成功标志
```
✓ TC-E2E-001 执行成功: 完整购物流程验证通过
✓ TC-E2E-002 执行成功: 多商品添加验证通过
...
----------------------------------------------------------------------
Ran 12 tests in 180.000s

OK
```

### 失败处理
1. 查看控制台输出的错误信息
2. 检查 `report/screenshot/` 中的截图
3. 根据截图和错误信息定位问题
4. 修复后重新运行测试

---

## 🔄 持续集成建议

### Jenkins/GitLab CI 配置示例

```yaml
# .gitlab-ci.yml
stages:
  - test

e2e_tests:
  stage: test
  script:
    - cd UI_Practice_Sauce_20260419
    - pip install -r requirements.txt
    - python -m pytest testcase/test_e2e_business_scenarios.py --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
    paths:
      - report/screenshot/
    when: always
```

---

## 📚 相关文档

- [all_testcases.xlsx](../exceltestcasedata/all_testcases.xlsx) - 业务场景测试用例清单
- [TEST_CASE_SYSTEM.md](../exceltestcasedata/TEST_CASE_SYSTEM.md) - 测试用例体系说明
- [README_EXCEL.md](../exceltestcasedata/README_EXCEL.md) - Excel 文件说明

---

## 💡 最佳实践

### 1. 定期执行
- **每日**: 执行 P0 用例（4个）
- **每周**: 执行 P0+P1 用例（10个）
- **版本发布前**: 执行全部用例（12个）

### 2. 维护建议
- UI 变更时及时更新元素定位器
- 新增业务场景时补充对应用例
- 定期 review 用例的有效性和覆盖率

### 3. 扩展方向
- 添加更多边界测试场景
- 集成性能测试（页面加载时间）
- 添加视觉回归测试

---

**文档版本**: v1.0  
**最后更新**: 2026-05-13  
**维护者**: 自动化测试团队
