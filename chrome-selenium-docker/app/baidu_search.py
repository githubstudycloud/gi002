#!/usr/bin/env python3
"""
百度搜索自动化脚本
"""

import os
import sys
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException


class BaiduSearchAutomation:
    """百度搜索自动化类"""

    def __init__(self, logger=None):
        self.driver = None
        self.logger = logger or self._setup_logger()

    def _setup_logger(self):
        """配置日志"""
        logger = logging.getLogger('BaiduSearch')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # 文件处理器
            fh = logging.FileHandler('/app/logs/baidu_search.log')
            fh.setLevel(logging.INFO)

            # 控制台处理器
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.INFO)

            # 格式化
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger

    def setup_chrome(self):
        """配置Chrome浏览器"""
        self.logger.info("初始化Chrome WebDriver")

        chrome_options = Options()

        # 从环境变量读取配置
        headless = os.getenv('CHROME_HEADLESS', 'true').lower() == 'true'
        no_sandbox = os.getenv('CHROME_NO_SANDBOX', 'true').lower() == 'true'
        disable_dev_shm = os.getenv('CHROME_DISABLE_DEV_SHM', 'true').lower() == 'true'

        # 基础选项
        if headless:
            chrome_options.add_argument('--headless=new')
            self.logger.info("启用无头模式")

        if no_sandbox:
            chrome_options.add_argument('--no-sandbox')

        if disable_dev_shm:
            chrome_options.add_argument('--disable-dev-shm-usage')

        # 性能和稳定性选项
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--lang=zh-CN')

        # 用户代理
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
        )

        # 下载配置
        prefs = {
            'download.default_directory': '/app/downloads',
            'download.prompt_for_download': False,
            'intl.accept_languages': 'zh-CN,zh',
        }
        chrome_options.add_experimental_option('prefs', prefs)

        # 排除自动化标志
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 创建WebDriver
        try:
            chromedriver_path = '/usr/local/bin/chromedriver'
            if not os.path.exists(chromedriver_path):
                self.logger.warning(f"ChromeDriver未找到在 {chromedriver_path}，使用系统PATH")
                service = Service()
            else:
                service = Service(executable_path=chromedriver_path)

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)

            self.logger.info("Chrome WebDriver初始化成功")

        except WebDriverException as e:
            self.logger.error(f"Chrome WebDriver初始化失败: {e}")
            raise

    def search_baidu(self, keyword="茶叶"):
        """
        在百度搜索指定关键词并返回第一条结果

        Args:
            keyword: 搜索关键词，默认为"茶叶"

        Returns:
            dict: 包含搜索结果的字典
        """
        result = {
            'success': False,
            'keyword': keyword,
            'first_result': None,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }

        try:
            if not self.driver:
                self.setup_chrome()

            self.logger.info(f"开始搜索: {keyword}")

            # 访问百度
            self.driver.get("https://www.baidu.com")
            self.logger.info("已访问百度首页")

            # 截图
            self.take_screenshot("baidu_homepage")

            # 查找搜索框
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "kw"))
            )

            if not search_box:
                raise Exception("未找到搜索框")

            # 输入搜索关键词
            search_box.clear()
            search_box.send_keys(keyword)
            self.logger.info(f"已输入搜索关键词: {keyword}")

            # 点击搜索按钮
            search_button = self.driver.find_element(By.ID, "su")
            search_button.click()
            self.logger.info("已点击搜索按钮")

            # 等待结果加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".result"))
            )

            # 截图
            self.take_screenshot("search_results")

            # 获取第一条搜索结果
            first_result = self.driver.find_element(By.CSS_SELECTOR, ".result")

            # 提取标题和链接
            try:
                title_element = first_result.find_element(By.TAG_NAME, "h3")
                title = title_element.text
            except NoSuchElementException:
                title = "无法获取标题"

            try:
                link_element = first_result.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
            except NoSuchElementException:
                link = "无法获取链接"

            try:
                abstract_element = first_result.find_element(By.CLASS_NAME, "c-abstract")
                abstract = abstract_element.text
            except NoSuchElementException:
                abstract = "无法获取摘要"

            result['first_result'] = {
                'title': title,
                'link': link,
                'abstract': abstract
            }
            result['success'] = True

            self.logger.info(f"搜索成功！第一条结果:")
            self.logger.info(f"  标题: {title}")
            self.logger.info(f"  链接: {link}")
            self.logger.info(f"  摘要: {abstract[:100]}...")

        except TimeoutException as e:
            error_msg = f"搜索超时: {str(e)}"
            self.logger.error(error_msg)
            result['error'] = error_msg
            self.take_screenshot("error_timeout")

        except Exception as e:
            error_msg = f"搜索过程出错: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            result['error'] = error_msg
            self.take_screenshot("error")

        return result

    def take_screenshot(self, name="screenshot"):
        """截图"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"/app/screenshots/{name}_{timestamp}.png"
            os.makedirs('/app/screenshots', exist_ok=True)
            self.driver.save_screenshot(filepath)
            self.logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            return None

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.logger.info("关闭Chrome WebDriver")
            try:
                self.driver.quit()
            except Exception as e:
                self.logger.error(f"关闭浏览器时出错: {e}")


def main():
    """主函数 - 用于测试"""
    automation = BaiduSearchAutomation()

    try:
        result = automation.search_baidu("茶叶")

        if result['success']:
            print("\n" + "=" * 60)
            print("搜索成功！")
            print("=" * 60)
            print(f"关键词: {result['keyword']}")
            print(f"标题: {result['first_result']['title']}")
            print(f"链接: {result['first_result']['link']}")
            print(f"摘要: {result['first_result']['abstract']}")
            print("=" * 60)
        else:
            print(f"\n搜索失败: {result['error']}")

    finally:
        automation.close()


if __name__ == "__main__":
    main()
