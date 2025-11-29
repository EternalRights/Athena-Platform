# framework/keyword_engine.py
from utils.logger import Logger
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
import time


class KeywordEngine:
    """关键字驱动引擎"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = Logger()
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)

        # 关键字映射
        self.keywords = {
            'open_login_page': self.open_login_page,
            'fill_username': self.fill_username,
            'fill_password': self.fill_password,
            'click_login': self.click_login,
            'verify_login_success': self.verify_login_success,
            'click_logout': self.click_logout,
            'verify_dashboard_loaded': self.verify_dashboard_loaded
        }

    def execute_keyword(self, keyword, data=None):
        """
        执行关键字
        :param keyword: 关键字名称
        :param data: 关键字数据
        :return: 执行结果
        """
        if keyword not in self.keywords:
            raise ValueError(f"未知关键字: {keyword}")

        self.logger.info(f"执行关键字: {keyword}, 数据: {data}")

        try:
            result = self.keywords[keyword](data)
            self.logger.info(f"关键字执行成功: {keyword}")
            return result
        except Exception as e:
            self.logger.error(f"关键字执行失败: {keyword}, 错误: {str(e)}")
            raise

    def open_login_page(self, data):
        """打开登录页面"""
        url = data.get('url', '/login') if data else '/login'
        self.login_page.open_login_page(url)
        return True

    def fill_username(self, data):
        """填写用户名"""
        if not data or 'value' not in data:
            raise ValueError("缺少用户名值")
        username = data['value']
        self.login_page.enter_username(username)
        return True

    def fill_password(self, data):
        """填写密码"""
        if not data or 'value' not in data:
            raise ValueError("缺少密码值")
        password = data['value']
        self.login_page.enter_password(password)
        return True

    def click_login(self, data):
        """点击登录"""
        self.login_page.click_login_button()
        time.sleep(2)  # 等待登录处理
        return True

    def verify_login_success(self, data):
        """验证登录成功"""
        expected_text = data.get('expected_text', 'Welcome') if data else 'Welcome'

        # 等待页面跳转
        time.sleep(3)

        # 检查是否在仪表板页面
        is_dashboard_loaded = self.dashboard_page.verify_dashboard_loaded()
        if not is_dashboard_loaded:
            raise AssertionError("登录后未跳转到仪表板页面")

        # 检查欢迎信息
        welcome_message = self.dashboard_page.get_welcome_message()
        if not welcome_message or expected_text not in welcome_message:
            raise AssertionError(f"未找到预期的欢迎信息 '{expected_text}', 实际: {welcome_message}")

        return True

    def click_logout(self, data):
        """点击退出"""
        self.dashboard_page.click_logout()
        time.sleep(2)
        return True

    def verify_dashboard_loaded(self, data):
        """验证仪表板已加载"""
        is_loaded = self.dashboard_page.verify_dashboard_loaded()
        if not is_loaded:
            raise AssertionError("仪表板页面未正确加载")
        return True

    def execute_test_scenario(self, scenario_data):
        """
        执行测试场景
        :param scenario_data: 场景数据列表，每个元素包含action和data
        """
        results = []
        for step in scenario_data:
            action = step.get('action')
            data = step.get('data', {})

            try:
                result = self.execute_keyword(action, data)
                results.append({
                    'action': action,
                    'status': 'PASS',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'action': action,
                    'status': 'FAIL',
                    'error': str(e)
                })
                # 如果步骤失败，可以选择继续或停止
                if not step.get('continue_on_failure', False):
                    break

        return results