import os

if os.getenv('DOCKER'):
    URL_WEBDRIVER = "http://172.17.0.1:4444/wd/hub"
else:
    URL_WEBDRIVER = "http://localhost:4444/wd/hub"
