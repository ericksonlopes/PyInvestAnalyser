from loguru import logger
from selenium import webdriver

logger.info('Iniciando bot Google')

options = webdriver.ChromeOptions()
chrome = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)

chrome.get('https://www.google.com')
print('chrome', chrome.title)
chrome.quit()
