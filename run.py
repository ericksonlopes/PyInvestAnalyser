import concurrent.futures
import csv

from src.models import Stock
from src.services import ExtractInfoFromStock

actives = [
    'B3SA3',
    'BBDC3',
    'BBSE3',
    'BMGB4'
]

result_actives = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(ExtractInfoFromStock().get_info_active, active) for active in actives]

    for future in concurrent.futures.as_completed(futures):
        try:
            active = future.result()

            if isinstance(active, str):
                active = ExtractInfoFromStock().get_active_keys_indicators(active)

            result_actives.append(active)

        except Exception as e:
            print(f'Error1: {str(e)}')

with open('result_for_actives.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(Stock().get_meaning_of_fields().values())

    for active in result_actives:
        writer.writerow(active.__dict__.values())


