from bs4 import Tag

from src.models import RealEstateFunds
from src.services.investidor_10.extract_info_abstract import ExtractActiveInformation


class ExtractInfoFromREF(ExtractActiveInformation):
    def __init__(self):
        super().__init__()

    def get_grade(self):
        return "-"

    def get_value_cell(self, cell: Tag) -> str:
        return cell.find("div", class_="value").text.replace("\n", "")

    def get_active_keys_indicators(self, active_name) -> RealEstateFunds:
        return RealEstateFunds(name=active_name, type="ref")

    def get_info_active(self, active_name: str) -> RealEstateFunds:
        ref = self.get_page_infos_for_active(active_name, "fiis")

        ret_ref = RealEstateFunds()
        list_keys_ref = list(RealEstateFunds().__dict__.keys())

        for num in range(len(list_keys_ref)):
            ret_ref.__dict__[list_keys_ref[num]] = list(ref.values())[num]

        return ret_ref
