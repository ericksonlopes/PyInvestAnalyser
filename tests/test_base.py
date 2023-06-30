from unittest import TestCase

from config import Logger


class BaseTestClass(TestCase):
    def setUp(self) -> None:
        self.logger = Logger(save_log=False).logger

    def tearDown(self) -> None:
        pass
