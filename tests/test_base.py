from unittest import TestCase

from config import Logger


class BaseTestClass(TestCase):
    def setUp(self) -> None:
        self.logger = Logger(save_log=False).logger

        self.stock_list = [
            'B3SA3',
            'BMGB4',

        ]
        self.ref_list = [
            'BIME11',
            'MXRF11',

        ]

        self.bdrs_list = [
            'AAPL34',
            'AMZO34'
        ]

    def tearDown(self) -> None:
        pass
