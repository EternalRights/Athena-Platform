# tests/conftest.py
import pytest
from framework.driver_manager import DriverManager
from framework.keyword_engine import KeywordEngine
from framework.data_driver import DataDriver
from utils.logger import Logger
import allure
import os


@pytest.fixture(scope="session")
def driver_manager():
    """WebDriver管理器fixture"""
    manager = DriverManager()
    yield manager
    manager.quit_driver()


@pytest.fixture(scope="function")
def driver(driver_manager):
    """WebDriver fixture，每个测试函数使用"""
    driver = driver_manager.get_driver()
    yield driver
    # 测试结束后清理
    driver.delete_all_cookies()


@pytest.fixture(scope="function")
def keyword_engine(driver):
    """关键字引擎fixture"""
    return KeywordEngine(driver)


@pytest.fixture(scope="session")
def data_driver():
    """数据驱动引擎fixture"""
    return DataDriver()


@pytest.fixture(autouse=True)
def setup_test(request, driver):
    """自动执行的测试设置"""
    # 在测试开始前执行
    test_name = request.node.name
    Logger().info(f"开始执行测试: {test_name}")

    yield  # 测试执行

    # 在测试结束后执行
    if request.node.rep_call.failed:
        # 如果测试失败，截图
        screenshot_path = os.path.join("reports", "screenshots", f"{test_name}_failure.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        Logger().error(f"测试失败，截图已保存: {screenshot_path}")
        allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

    Logger().info(f"测试执行完成: {test_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """钩子函数，用于捕获测试结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)