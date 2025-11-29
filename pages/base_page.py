# pages/base_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.element_locator import ElementLocator
from utils.logger import Logger
import time
import os


class BasePage:
    """页面对象基类，封装通用页面操作"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.locator = ElementLocator()
        self.logger = Logger()

    def find_element(self, locator_data, timeout=10):
        """
        智能查找元素，支持多种定位策略
        :param locator_data: 定位数据列表
        :param timeout: 超时时间
        :return: WebElement对象
        """
        return self.locator.find_element(self.driver, locator_data, timeout)

    def find_elements(self, locator_data, timeout=10):
        """
        智能查找多个元素
        :param locator_data: 定位数据列表
        :param timeout: 超时时间
        :return: WebElement对象列表
        """
        return self.locator.find_elements(self.driver, locator_data, timeout)

    def click_element(self, locator_data, timeout=10):
        """点击元素"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(self.locator.get_selenium_locator(locator_data))
            )
            element.click()
            self.logger.info(f"成功点击元素: {locator_data}")
        except TimeoutException:
            self.logger.error(f"点击元素超时: {locator_data}")
            raise

    def input_text(self, locator_data, text, timeout=10):
        """输入文本"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located(self.locator.get_selenium_locator(locator_data))
            )
            element.clear()
            element.send_keys(text)
            self.logger.info(f"成功输入文本 '{text}' 到元素: {locator_data}")
        except TimeoutException:
            self.logger.error(f"输入文本超时: {locator_data}")
            raise

    def get_text(self, locator_data, timeout=10):
        """获取元素文本"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located(self.locator.get_selenium_locator(locator_data))
            )
            text = element.text
            self.logger.info(f"获取元素文本成功: {text}")
            return text
        except TimeoutException:
            self.logger.error(f"获取元素文本超时: {locator_data}")
            raise

    def wait_for_element_visible(self, locator_data, timeout=10):
        """等待元素可见"""
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(self.locator.get_selenium_locator(locator_data))
            )
            self.logger.info(f"元素已可见: {locator_data}")
            return element
        except TimeoutException:
            self.logger.error(f"等待元素可见超时: {locator_data}")
            raise

    def take_screenshot(self, filename):
        """截图"""
        screenshot_dir = "reports/screenshots/"
        os.makedirs(screenshot_dir, exist_ok=True)
        filepath = os.path.join(screenshot_dir, f"{filename}.png")
        self.driver.save_screenshot(filepath)
        self.logger.info(f"截图已保存: {filepath}")
        return filepath

    def scroll_to_element(self, locator_data):
        """滚动到元素"""
        element = self.find_element(locator_data)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.logger.info(f"已滚动到元素: {locator_data}")

    def execute_js(self, script, *args):
        """执行JavaScript"""
        result = self.driver.execute_script(script, *args)
        self.logger.info(f"执行JS成功: {script}")
        return result