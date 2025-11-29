# utils/element_locator.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger
import time


class ElementLocator:
    """动态元素定位工具类"""

    def __init__(self):
        self.logger = Logger()
        self.locator_mapping = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }

    def get_selenium_locator(self, locator_data):
        """
        将定位数据转换为Selenium定位器
        :param locator_data: 定位数据（可以是单个字典或字典列表）
        :return: Selenium定位器元组 (By, value)
        """
        if isinstance(locator_data, list):
            # 如果是列表，取第一个有效的定位器
            for locator in locator_data:
                if isinstance(locator, dict) and 'type' in locator and 'value' in locator:
                    locator_type = locator['type']
                    locator_value = locator['value']
                    if locator_type in self.locator_mapping:
                        return (self.locator_mapping[locator_type], locator_value)
        elif isinstance(locator_data, dict):
            # 如果是单个字典
            locator_type = locator_data['type']
            locator_value = locator_data['value']
            if locator_type in self.locator_mapping:
                return (self.locator_mapping[locator_type], locator_value)

        raise ValueError(f"无效的定位数据: {locator_data}")

    def find_element(self, driver, locator_data, timeout=10):
        """
        智能查找元素，支持多重定位策略
        :param driver: WebDriver实例
        :param locator_data: 定位数据列表
        :param timeout: 超时时间
        :return: WebElement对象
        """
        if not isinstance(locator_data, list):
            locator_data = [locator_data]

        wait = WebDriverWait(driver, timeout)

        for i, locator in enumerate(locator_data):
            try:
                selenium_locator = self.get_selenium_locator(locator)
                element = wait.until(
                    EC.presence_of_element_located(selenium_locator)
                )
                self.logger.info(f"使用定位策略 {i + 1}/{len(locator_data)} 成功找到元素: {locator}")
                return element
            except TimeoutException:
                if i == len(locator_data) - 1:  # 如果是最后一个策略
                    self.logger.error(f"所有定位策略均失败: {locator_data}")
                    raise TimeoutException(f"无法找到元素: {locator_data}")
                else:
                    self.logger.warning(f"定位策略 {i + 1} 失败，尝试下一个: {locator}")
                    continue

        raise TimeoutException(f"无法找到元素: {locator_data}")

    def find_elements(self, driver, locator_data, timeout=10):
        """
        智能查找多个元素
        :param driver: WebDriver实例
        :param locator_data: 定位数据
        :param timeout: 超时时间
        :return: WebElement对象列表
        """
        selenium_locator = self.get_selenium_locator(locator_data)
        wait = WebDriverWait(driver, timeout)

        try:
            elements = wait.until(
                EC.presence_of_all_elements_located(selenium_locator)
            )
            self.logger.info(f"找到 {len(elements)} 个元素: {locator_data}")
            return elements
        except TimeoutException:
            self.logger.error(f"无法找到元素列表: {locator_data}")
            raise

    def wait_for_element_clickable(self, driver, locator_data, timeout=10):
        """等待元素可点击"""
        selenium_locator = self.get_selenium_locator(locator_data)
        wait = WebDriverWait(driver, timeout)

        try:
            element = wait.until(
                EC.element_to_be_clickable(selenium_locator)
            )
            self.logger.info(f"元素可点击: {locator_data}")
            return element
        except TimeoutException:
            self.logger.error(f"元素不可点击: {locator_data}")
            raise

    def smart_find_and_interact(self, driver, locator_data, interaction_type='click', timeout=10):
        """
        智能查找并交互（点击、输入等）
        :param driver: WebDriver实例
        :param locator_data: 定位数据
        :param interaction_type: 交互类型 ('click', 'send_keys', 'get_text')
        :param timeout: 超时时间
        :return: 交互结果
        """
        element = self.find_element(driver, locator_data, timeout)

        if interaction_type == 'click':
            element.click()
            return True
        elif interaction_type == 'send_keys':
            return element
        elif interaction_type == 'get_text':
            return element.text
        else:
            raise ValueError(f"不支持的交互类型: {interaction_type}")