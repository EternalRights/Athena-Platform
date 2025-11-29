# framework/driver_manager.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utils.logger import Logger
import yaml
import os


class DriverManager:
    """WebDriver管理器"""

    def __init__(self, config_path="config/config.yaml"):
        self.logger = Logger()
        self.config = self._load_config(config_path)
        self.driver = None

    def _load_config(self, config_path):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def create_driver(self):
        """创建WebDriver实例"""
        browser_name = self.config['browser']['name'].lower()

        if browser_name == 'chrome':
            self.driver = self._create_chrome_driver()
        elif browser_name == 'firefox':
            self.driver = self._create_firefox_driver()
        elif browser_name == 'edge':
            self.driver = self._create_edge_driver()
        else:
            raise ValueError(f"不支持的浏览器: {browser_name}")

        self._configure_driver()
        self.logger.info(f"WebDriver创建成功: {browser_name}")
        return self.driver

    def _create_chrome_driver(self):
        """创建Chrome驱动"""
        options = Options()

        if self.config['browser']['headless']:
            options.add_argument('--headless')

        if self.config['browser']['maximize']:
            options.add_argument('--start-maximized')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        # 可以根据需要添加更多选项
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])

        return webdriver.Chrome(options=options)

    def _create_firefox_driver(self):
        """创建Firefox驱动"""
        options = FirefoxOptions()

        if self.config['browser']['headless']:
            options.add_argument('--headless')

        return webdriver.Firefox(options=options)

    def _create_edge_driver(self):
        """创建Edge驱动"""
        options = EdgeOptions()

        if self.config['browser']['headless']:
            options.add_argument('--headless')

        if self.config['browser']['maximize']:
            options.add_argument('--start-maximized')

        options.add_argument('--window-size=1920,1080')

        return webdriver.Edge(options=options)

    def _configure_driver(self):
        """配置驱动参数"""
        # 设置隐式等待
        implicit_wait = self.config['browser']['implicit_wait']
        self.driver.implicitly_wait(implicit_wait)

        # 设置页面加载超时
        page_load_timeout = self.config['browser']['page_load_timeout']
        self.driver.set_page_load_timeout(page_load_timeout)

        self.logger.info(f"Driver配置完成 - 隐式等待: {implicit_wait}s, 页面加载超时: {page_load_timeout}s")

    def quit_driver(self):
        """退出驱动"""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver已退出")
            self.driver = None

    def get_driver(self):
        """获取当前驱动实例"""
        if not self.driver:
            self.create_driver()
        return self.driver