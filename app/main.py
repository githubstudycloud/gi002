#!/usr/bin/env python3
"""
Chrome Selenium自动化示例脚本
"""

import os
import sys
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ChromeAutomation:
    """Chrome自动化基类"""

    def __init__(self):
        self.driver = None
        self.setup_chrome()

    def setup_chrome(self):
        """配置Chrome选项"""
        logger.info("初始化Chrome WebDriver")

        chrome_options = Options()

        # 从环境变量读取配置
        headless = os.getenv('CHROME_HEADLESS', 'true').lower() == 'true'
        no_sandbox = os.getenv('CHROME_NO_SANDBOX', 'true').lower() == 'true'
        disable_dev_shm = os.getenv('CHROME_DISABLE_DEV_SHM', 'true').lower() == 'true'

        # 基础选项
        if headless:
            chrome_options.add_argument('--headless=new')
            logger.info("启用无头模式")

        if no_sandbox:
            chrome_options.add_argument('--no-sandbox')

        if disable_dev_shm:
            chrome_options.add_argument('--disable-dev-shm-usage')

        # 性能和稳定性选项
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--window-size=1920,1080')

        # 用户代理
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        )

        # 下载配置
        prefs = {
            'download.default_directory': '/app/downloads',
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True,
            'profile.default_content_setting_values.notifications': 2,  # 禁用通知
        }
        chrome_options.add_experimental_option('prefs', prefs)

        # 排除自动化标志
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 创建WebDriver
        try:
            # 检查ChromeDriver路径
            chromedriver_path = '/usr/local/bin/chromedriver'
            if not os.path.exists(chromedriver_path):
                logger.warning(f"ChromeDriver未找到在 {chromedriver_path}，使用系统PATH")
                service = Service()
            else:
                service = Service(executable_path=chromedriver_path)

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)

            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)

            logger.info("Chrome WebDriver初始化成功")

        except WebDriverException as e:
            logger.error(f"Chrome WebDriver初始化失败: {e}")
            raise

    def take_screenshot(self, name="screenshot"):
        """截图"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"/app/screenshots/{name}_{timestamp}.png"
            self.driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None

    def wait_for_element(self, by, value, timeout=10):
        """等待元素出现"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"等待元素超时: {by}={value}")
            return None

    def close(self):
        """关闭浏览器"""
        if self.driver:
            logger.info("关闭Chrome WebDriver")
            self.driver.quit()


class GoogleSearchExample(ChromeAutomation):
    """Google搜索示例"""

    def run(self, search_term="Selenium WebDriver"):
        """执行搜索"""
        try:
            logger.info(f"开始搜索: {search_term}")

            # 访问Google
            self.driver.get("https://www.google.com")
            logger.info("已访问Google首页")

            # 截图
            self.take_screenshot("google_homepage")

            # 查找搜索框
            search_box = self.wait_for_element(By.NAME, "q")
            if not search_box:
                logger.error("未找到搜索框")
                return False

            # 输入搜索关键词
            search_box.send_keys(search_term)
            search_box.submit()
            logger.info(f"已提交搜索: {search_term}")

            # 等待结果加载
            time.sleep(2)

            # 截图
            self.take_screenshot("search_results")

            # 获取搜索结果
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
            logger.info(f"找到 {len(results)} 个搜索结果")

            # 打印前5个结果
            for i, result in enumerate(results[:5], 1):
                logger.info(f"结果 {i}: {result.text}")

            logger.info("搜索任务完成")
            return True

        except Exception as e:
            logger.error(f"搜索过程出错: {e}")
            self.take_screenshot("error")
            return False


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("Chrome Selenium自动化任务开始")
    logger.info("=" * 60)

    # 创建必要的目录
    os.makedirs('/app/screenshots', exist_ok=True)
    os.makedirs('/app/downloads', exist_ok=True)

    automation = None
    try:
        # 创建自动化实例
        automation = GoogleSearchExample()

        # 执行搜索
        success = automation.run("Python Selenium Docker")

        if success:
            logger.info("任务执行成功")
        else:
            logger.warning("任务执行失败")

        # 保持运行一段时间（可选）
        keep_alive = os.getenv('KEEP_ALIVE', 'false').lower() == 'true'
        if keep_alive:
            logger.info("容器保持运行状态...")
            while True:
                time.sleep(60)

    except KeyboardInterrupt:
        logger.info("收到中断信号，正在退出...")

    except Exception as e:
        logger.error(f"发生错误: {e}", exc_info=True)
        sys.exit(1)

    finally:
        if automation:
            automation.close()

        logger.info("=" * 60)
        logger.info("Chrome Selenium自动化任务结束")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
