import os

from loguru import logger


class Logger:
    def __init__(self):
        self.logger = logger
        # logger.remove()

        __ABSOLUTE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))

        if not os.path.exists(__ABSOLUTE_PATH):
            os.makedirs(__ABSOLUTE_PATH)

        # self.logger.add(os.path.join(__ABSOLUTE_PATH, 'logs.log'))
        # self.logger.add(os.path.join(__ABSOLUTE_PATH, 'logs_json.log'), serialize=True)
