from src.services import ExtractInfoFromREF, ExtractInfoFromBDR, ExtractInfoFromStock


def generate_single():
    ExtractInfoFromREF().get_info_active('vigt11')
    ExtractInfoFromStock().get_info_active('vale3')
    ExtractInfoFromBDR().get_info_active('MSFT34')
