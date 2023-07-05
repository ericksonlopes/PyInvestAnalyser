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
        ret_ref = RealEstateFunds()
        ret_ref.name = active_name

        try:
            ref = self.get_page_infos_for_active(active_name, "fiis")

            list_keys_ref = list(RealEstateFunds().__dict__.keys())

            for key, value in ref.items():
                if key in list_keys_ref:
                    ret_ref.__dict__[key] = value

                mean = ret_ref.get_meaning_of_fields()

                if key in mean.values():
                    key_mean = list(mean.keys())[list(mean.values()).index(key)]
                    ret_ref.__dict__[key_mean] = value

        except Exception as e:
            self.logger.error(f"Error to get information for active {active_name}")
            self.logger.error(e)

        finally:
            self.logger.info(f"Information for active {active_name} successfully obtained")

        return ret_ref
