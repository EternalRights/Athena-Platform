# tests/test_login.py
import pytest
from framework.data_driver import DataDriver
import allure


@allure.feature("用户登录功能")
class TestLogin:
    """登录功能测试"""

    def test_valid_login(self, keyword_engine, data_driver):
        """测试有效凭据登录"""
        with allure.step("获取测试数据"):
            test_data = data_driver.get_login_test_data('valid_credentials')[0]
            username = test_data['username']
            password = test_data['password']

        with allure.step("执行登录流程"):
            keyword_engine.execute_keyword('open_login_page', {'url': '/login'})
            keyword_engine.execute_keyword('fill_username', {'value': username})
            keyword_engine.execute_keyword('fill_password', {'value': password})
            keyword_engine.execute_keyword('click_login', {})

        with allure.step("验证登录成功"):
            keyword_engine.execute_keyword('verify_login_success', {'expected_text': 'Welcome'})

    @pytest.mark.parametrize("credentials", [
        {"username": "invalid@example.com", "password": "wrongpass", "expected_result": "failure"},
        {"username": "", "password": "", "expected_result": "failure"},
        {"username": "nonexistent@user.com", "password": "anypassword", "expected_result": "failure"}
    ])
    @allure.story("无效登录凭据")
    def test_invalid_login(self, keyword_engine, data_driver, credentials):
        """测试无效凭据登录"""
        username = credentials['username']
        password = credentials['password']

        with allure.step(f"使用无效凭据登录: {username}"):
            keyword_engine.execute_keyword('open_login_page', {'url': '/login'})
            keyword_engine.execute_keyword('fill_username', {'value': username})
            keyword_engine.execute_keyword('fill_password', {'value': password})
            keyword_engine.execute_keyword('click_login', {})

        with allure.step("验证登录失败"):
            # 这里应该验证登录失败的场景
            # 具体实现取决于应用的错误处理方式
            pass

    @allure.story("登录流程完整场景")
    def test_login_logout_scenario(self, keyword_engine, data_driver):
        """测试完整的登录-使用-退出场景"""
        # 获取有效登录数据
        valid_data = data_driver.get_login_test_data('valid_credentials')[0]
        username = valid_data['username']
        password = valid_data['password']

        with allure.step("执行登录"):
            keyword_engine.execute_keyword('open_login_page', {'url': '/login'})
            keyword_engine.execute_keyword('fill_username', {'value': username})
            keyword_engine.execute_keyword('fill_password', {'value': password})
            keyword_engine.execute_keyword('click_login', {})

        with allure.step("验证登录成功并检查仪表板"):
            keyword_engine.execute_keyword('verify_login_success', {'expected_text': 'Welcome'})
            keyword_engine.execute_keyword('verify_dashboard_loaded', {})

        with allure.step("执行退出登录"):
            keyword_engine.execute_keyword('click_logout', {})

    @allure.story("数据驱动登录测试")
    def test_data_driven_login(self, keyword_engine, data_driver):
        """数据驱动的登录测试"""
        valid_logins = data_driver.get_login_test_data('valid_credentials')

        for i, credentials in enumerate(valid_logins):
            with allure.step(f"数据驱动测试 - 案例 {i + 1}"):
                username = credentials['username']
                password = credentials['password']

                # 打开登录页面
                keyword_engine.execute_keyword('open_login_page', {'url': '/login'})

                # 输入凭据并登录
                keyword_engine.execute_keyword('fill_username', {'value': username})
                keyword_engine.execute_keyword('fill_password', {'value': password})
                keyword_engine.execute_keyword('click_login', {})

                # 验证登录成功
                keyword_engine.execute_keyword('verify_login_success', {'expected_text': 'Welcome'})

                # 退出登录以便下一次测试
                keyword_engine.execute_keyword('click_logout', {})


if __name__ == "__main__":
    pytest.main(['-v', __file__])