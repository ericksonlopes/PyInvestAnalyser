from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from config import URL_WEBDRIVER


def get_webdriver() -> WebDriver:
    options = webdriver.ChromeOptions()

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    return webdriver.Remote(command_executor=URL_WEBDRIVER, options=options)
