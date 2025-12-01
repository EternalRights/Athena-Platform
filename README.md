# Web自动化测试平台

## 项目概述

这是一个基于Selenium和pytest构建的Web应用自动化测试平台，采用数据驱动与关键字驱动的混合测试框架，旨在提高回归测试效率，减少人工测试成本。

## 项目特点

- **混合测试框架**: 结合数据驱动和关键字驱动的优势
- **Page Object模式**: 页面元素与测试逻辑解耦，提升代码复用性
- **智能元素定位**: 多重定位策略，解决Ajax加载问题
- **统一配置管理**: YAML配置中心，实现数据与业务逻辑分离
- **异常处理机制**: 自动重试和错误日志记录
- **集成报告系统**: Allure报告和Jenkins持续集成

## 项目结构
## 各目录说明

### 📁 config/ - 配置文件
- `config.yaml` - 主配置文件（数据库连接、环境配置等）
- `test_data.yaml` - 测试数据文件

### 📁 pages/ - 页面对象模型
- `base_page.py` - 基础页面类（封装通用方法）
- `login_page.py` - 登录页面对象
- `dashboard_page.py` - 仪表板页面对象

### 📁 tests/ - 测试用例
- `conftest.py` - pytest配置和fixture
- `test_login.py` - 登录功能测试用例
- `test_dashboard.py` - 仪表板功能测试用例

### 📁 utils/ - 工具类
- `element_locator.py` - 元素定位工具
- `logger.py` - 日志记录工具
- `report_generator.py` - 测试报告生成器

### 📁 framework/ - 框架核心
- `driver_manager.py` - 浏览器驱动管理
- `keyword_engine.py` - 关键字驱动引擎
- `data_driver.py` - 数据驱动引擎

### 📁 reports/ - 测试报告输出目录

### 📁 jenkins/ - Jenkins持续集成配置


## 技术栈

- **Python 3.8+**
- **Selenium 4.x** - Web自动化测试
- **pytest** - 测试框架
- **Allure** - 报告生成
- **PyYAML** - 配置文件解析
- **Page Object Model** - 设计模式

## 安装与配置

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd web-automation-platform

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate    # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置修改
修改 config/config.yaml 中的浏览器配置和测试环境：
```Yaml
browser:
  name: "chrome"        # 浏览器类型
  headless: false       # 是否无头模式
  maximize: true        # 是否最大化窗口

environment:
  base_url: "https://your-test-url.com"  # 测试环境URL
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_login.py

# 生成Allure报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 核心功能

### 1.智能元素定位

支持多种定位策略，自动重试机制：

```python
# 配置多种定位方式
page_elements = {
    'login_button': [
        {'type': 'id', 'value': 'loginBtn'},
        {'type': 'xpath', 'value': "//button[contains(text(), 'Login')]"},
        {'type': 'css', 'value': "button.login-button"}
    ]
}
```

### 2.数据驱动测试

通过YAML文件管理测试数据：

```Yaml
login_test_data:
  valid_credentials:
    - username: "testuser@example.com"
      password: "password123"
      expected_result: "success"
```

### 3.关键字驱动

通过关键字执行测试步骤：

```python
keywords = {
    'open_login_page': self.open_login_page,
    'fill_username': self.fill_username,
    'click_login': self.click_login
}
```

## 项目成果

- 回归测试时间从10小时缩短至3.2小时，效率提升60%
- 自动化测试覆盖率从30%提升至85%
- 用例执行成功率稳定在98%以上
- 缺陷拦截率提高至75%

## Jenkins集成

配置Jenkinsfile实现持续集成：

```grooy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/web-automation-platform.git'
            }
        }
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --alluredir=reports/allure-results'
            }
        }
        stage('Report') {
            steps {
                sh 'allure generate reports/allure-results -o reports/allure-report'
            }
        }
    }
}
```

## 维护与扩展

- 新增页面：继承BasePage，实现页面特定方法
- 添加测试用例：按照Page Object模式编写
- 扩展关键字：在KeywordEngine中添加新的关键字方法

## 许可证

本项目采用 MIT 许可证
