import concurrent.futures
import csv

from src.ExtractActive import ExtractInfoFromStock
from src.models import Stock

actives = [
    # {"active": 'AAPL34', "type": "bdrs"},
    {"active": 'B3SA3', "type": "acoes"},
    {"active": 'BBDC3', "type": "acoes"},
    {"active": 'BBSE3', "type": "acoes"},
    # {"active": 'BIME11', "type": "fiis"},
    # {"active": 'MXRF11', "type": "fiis"},
    # {"active": 'SNAG11', "type": "fiis"},
    {"active": 'BMGB4', "type": "acoes"},
]

result_actives = []

# print(ExtractInfoFromStock().get_info_active("B3SA3"))

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(ExtractInfoFromStock().get_info_active, active["active"]) for active in actives]

    for future in concurrent.futures.as_completed(futures):
        try:
            active = future.result()
            print(active)
            result_actives.append(active)

        except Exception as e:
            print(f'Error1: {str(e)}')

with open('result_for_actives.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(Stock().get_meaning_of_fields().values())

    for active in result_actives:
        writer.writerow(active.__dict__.values())
