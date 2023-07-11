import concurrent.futures

import pandas as pd

from config import Logger
from src.services import ExtractInfoFromREF, ExtractInfoFromBDR, ExtractInfoFromStock


def generate_csv(actives):
    result_actives = []

    logger = Logger().logger

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ExtractInfoFromREF().get_info_active, active) for active in actives]

        for future in concurrent.futures.as_completed(futures):

            try:
                active = future.result()

                if isinstance(active, str):
                    active = ExtractInfoFromREF().get_active_keys_indicators(active)

                result_actives.append(active)
            except Exception as e:
                logger.error(f"Error to get information for active {active.name}")
                logger.error(e)

    return pd.DataFrame(result_actives)


def generate_single():
    ExtractInfoFromREF().get_info_active('vigt11')
    ExtractInfoFromStock().get_info_active('vale3')
    ExtractInfoFromBDR().get_info_active('MSFT34')
