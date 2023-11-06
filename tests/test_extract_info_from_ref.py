import concurrent.futures

import pytest

from py_invest_analyser.services import ExtractInfoFromREF
from tests.test_base import BaseTestClass


class TestExtractInfoREF(BaseTestClass):
    @pytest.mark.ref
    def test_get_info_active(self):
        result_actives = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ExtractInfoFromREF().get_info_active, active) for active in self.ref_list]

            for future in concurrent.futures.as_completed(futures):
                try:
                    active = future.result()

                    if isinstance(active, str):
                        active = ExtractInfoFromREF().get_active_keys_indicators(active)

                    result_actives.append(active)

                except Exception:
                    assert False

                finally:
                    assert True
