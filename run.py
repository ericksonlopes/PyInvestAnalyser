import concurrent.futures
import csv

from config import Logger
from src.models import RealEstateFunds
from src.services import ExtractInfoFromREF, ExtractInfoFromBDR, ExtractInfoFromStock


def generate_csv():
    actives = [
        'HGLG11',
        'KNCR11',
        'MXRF11',
        'RBFF11',
        'SNAG11',
        'XPSF11',
        "HSML11",
        "VINO11",
    ]

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

    with open('result_for_actives.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(RealEstateFunds().get_meaning_of_fields().values())

        for active in result_actives:
            writer.writerow(active.__dict__.values())


def generate_single():
    ExtractInfoFromREF().get_info_active('vigt11')
    ExtractInfoFromStock().get_info_active('vale3')
    ExtractInfoFromBDR().get_info_active('MSFT34')


if __name__ == '__main__':
    generate_csv()
    # generate_single()
    # adicionando mais logs e tratando area que pega os dados do site e distribui no objeto
