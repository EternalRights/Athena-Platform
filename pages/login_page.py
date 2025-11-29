# pages/login_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class LoginPage(BasePage):
    """登录页面对象"""

    def __init__(self, driver):
        super().__init__(driver)
        self.page_elements = {
            'username_input': [
                {'type': 'id', 'value': 'username'},
                {'type': 'name', 'value': 'email'},
                {'type': 'css', 'value': "input[type='email']"}
            ],
            'password_input': [
                {'type': 'id', 'value': 'password'},
                {'type': 'name', 'value': 'password'},
                {'type': 'css', 'value': "input[type='password']"}
            ],
            'login_button': [
                {'type': 'id', 'value': 'loginBtn'},
                {'type': 'xpath', 'value': "//button[contains(text(), 'Login')]"},
                {'type': 'css', 'value': "button.login-button"}
            ],
            'error_message': [
                {'type': 'class', 'value': 'error-message'},
                {'type': 'xpath', 'value': "//div[@class='alert alert-danger']"}
            ]
        }

    def open_login_page(self, url="/login"):
        """打开登录页面"""
        full_url = self.driver.current_url.rsplit('/', 1)[0] + url
        self.driver.get(full_url)
        self.logger.info(f"打开登录页面: {full_url}")
        time.sleep(1)  # 等待页面加载

    def enter_username(self, username):
        """输入用户名"""
        self.input_text(self.page_elements['username_input'], username)

    def enter_password(self, password):
        """输入密码"""
        self.input_text(self.page_elements['password_input'], password)

    def click_login_button(self):
        """点击登录按钮"""
        self.click_element(self.page_elements['login_button'])

    def login(self, username, password):
        """完整登录流程"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self):
        """获取错误信息"""
        try:
            error_element = self.find_element(self.page_elements['error_message'])
            return error_element.text
        except:
            return None

    def is_login_successful(self):
        """检查是否登录成功（通过URL变化判断）"""
        current_url = self.driver.current_url
        # 假设登录成功后URL会变化，这里可以根据实际项目调整
        success_indicators = ['/dashboard', '/home', '/profile']
        return any(indicator in current_url for indicator in success_indicators)