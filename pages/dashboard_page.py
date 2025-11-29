# pages/dashboard_page.py
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """仪表板页面对象"""

    def __init__(self, driver):
        super().__init__(driver)
        self.page_elements = {
            'welcome_message': [
                {'type': 'xpath', 'value': "//h1[contains(text(), 'Welcome')]"},
                {'type': 'css', 'value': '.welcome-message'},
                {'type': 'class', 'value': 'user-greeting'}
            ],
            'logout_button': [
                {'type': 'id', 'value': 'logout'},
                {'type': 'css', 'value': "button.logout-btn"},
                {'type': 'xpath', 'value': "//a[contains(text(), 'Logout') or contains(text(), '退出')]"}
            ],
            'user_profile': [
                {'type': 'id', 'value': 'user-profile'},
                {'type': 'css', 'value': '.user-info'},
                {'type': 'class', 'value': 'profile-menu'}
            ]
        }

    def get_welcome_message(self):
        """获取欢迎信息"""
        try:
            message_element = self.find_element(self.page_elements['welcome_message'])
            return message_element.text
        except:
            return None

    def click_logout(self):
        """点击退出登录"""
        self.click_element(self.page_elements['logout_button'])

    def verify_dashboard_loaded(self):
        """验证仪表板页面已加载"""
        try:
            self.wait_for_element_visible(self.page_elements['welcome_message'])
            return True
        except:
            return False

    def get_user_profile_info(self):
        """获取用户资料信息"""
        try:
            profile_element = self.find_element(self.page_elements['user_profile'])
            return profile_element.text
        except:
            return None