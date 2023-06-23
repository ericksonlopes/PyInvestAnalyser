from selenium import webdriver

from settings.web_driver.download_webdriver import download_webdriver


def get_webdriver():
    path_webdriver = download_webdriver()

    if not path_webdriver:
        exit()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    return webdriver.Chrome(options=options)
