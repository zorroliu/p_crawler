# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from base.config import default_config


def get_chrome_driver():
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # =>去掉浏览器正在受到自动测试软件的控制
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # 为Chrome配置无头模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 禁用启用Blink运行时的功能
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    service = Service(executable_path=default_config.get_val('chrome_driver_path'))

    return webdriver.Chrome(options=chrome_options, service=service)
