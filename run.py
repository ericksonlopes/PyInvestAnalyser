from pprint import pprint

from src.services import ExtractInfoFromREF, ExtractInfoFromBDR, ExtractInfoFromStock


def generate_single():
    try:
        pprint(ExtractInfoFromREF().get_info_active('tord11'))
        pprint(ExtractInfoFromStock().get_info_active('vale3'))
        pprint(ExtractInfoFromBDR().get_info_active('MSFT34'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    generate_single()
