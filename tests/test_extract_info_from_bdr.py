from src.services import ExtractInfoFromBDR
from tests.test_base import BaseTestClass


class TestExtractInfoBDR(BaseTestClass):
    def test_get_info_active(self):
        try:
            ExtractInfoFromBDR().get_info_active("AAPL34")
        except Exception:
            assert False
        finally:
            assert True
