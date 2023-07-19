from src.services import ExtractInfoFromREF, ExtractInfoFromBDR, ExtractInfoFromStock
from pprint import pprint


def generate_single():
    pprint(ExtractInfoFromREF().get_info_active('tord11'))
    pprint(ExtractInfoFromStock().get_info_active('vale3'))
    pprint(ExtractInfoFromBDR().get_info_active('MSFT34'))


if __name__ == '__main__':
    generate_single()
