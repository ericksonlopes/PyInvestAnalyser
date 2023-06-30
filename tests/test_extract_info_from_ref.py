from src.services import ExtractInfoFromREF
from tests.test_base import BaseTestClass


class TestExtractInfoREF(BaseTestClass):
    def test_get_info_active(self):
        try:
            ExtractInfoFromREF().get_info_active("MXRF11")
        except Exception:
            assert False
        finally:
            assert True
