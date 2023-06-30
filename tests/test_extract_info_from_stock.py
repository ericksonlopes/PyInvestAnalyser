from src.services import ExtractInfoFromStock
from tests.test_base import BaseTestClass


class TestExtractInfoStock(BaseTestClass):
    def test_get_info_active(self):
        try:
            ExtractInfoFromStock().get_info_active("PETR4")
        except Exception:
            assert False
        finally:
            assert True
