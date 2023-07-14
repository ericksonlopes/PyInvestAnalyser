import concurrent.futures

import pytest

from src.services import ExtractInfoFromBDR
from tests.test_base import BaseTestClass


class TestExtractInfoBDR(BaseTestClass):

    @pytest.mark.bdr
    def test_get_info_active(self):
        result_actives = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ExtractInfoFromBDR().get_info_active, active) for active in self.bdrs_list]

            for future in concurrent.futures.as_completed(futures):
                try:
                    active = future.result()

                    if isinstance(active, str):
                        active = ExtractInfoFromBDR().get_active_keys_indicators(active)

                    result_actives.append(active)

                except Exception:
                    assert False

                finally:
                    assert True
