from bs4 import Tag

from src.models import BDR
from src.services.investidor_10.extract_info_abstract import ExtractActiveInformation


class ExtractInfoFromBDR(ExtractActiveInformation):
    def __init__(self):
        super().__init__()

    def get_grade(self):
        return "-"

    def get_value_cell(self, cell: Tag):
        return cell.div.text.replace("\n", "")

    def get_active_keys_indicators(self, active_name) -> BDR:
        return BDR(name=active_name, type="bdrs")

    def get_info_active(self, active_name: str) -> BDR:
        bdr = self.get_page_infos_for_active(active_name, "bdrs")

        ret_bdr = BDR()
        list_bdr_keys = list(BDR().__dict__.keys())

        for num in range(len(list_bdr_keys)):
            ret_bdr.__dict__[list_bdr_keys[num]] = list(bdr.values())[num]

        return ret_bdr
