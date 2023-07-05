from bs4 import Tag

from src.models import Stock
from src.services.investidor_10.extract_info_abstract import ExtractActiveInformation


class ExtractInfoFromStock(ExtractActiveInformation):
    def __init__(self):
        super().__init__()

    def get_value_cell(self, cell: Tag):
        return cell.div.text.replace("\n", "")

    def get_active_keys_indicators(self, active_name) -> Stock:
        return Stock(name=active_name, type="acoes")

    def get_grade(self):
        grade = self.soup.find('div', id="checklist").find('div', class_='rating')
        grade_text = grade.text.replace("\n", "").replace(" ", "").replace("Nota", "").replace(":", "")
        return grade_text

    def get_info_active(self, active_name) -> Stock:
        ret_stock = Stock()
        ret_stock.name = active_name

        try:
            stock = self.get_page_infos_for_active(active_name, "acoes")

            list_keys_ref = list(Stock().__dict__.keys())

            for key, value in stock.items():
                key = key.rstrip()

                if key in list_keys_ref:
                    ret_stock.__dict__[key] = value

                mean = ret_stock.get_meaning_of_fields()

                if key in mean.values():
                    key_mean = list(mean.keys())[list(mean.values()).index(key)]
                    ret_stock.__dict__[key_mean] = value

        except Exception as e:
            self.logger.error(f"Error to get information for active {active_name}")
            self.logger.error(e)

        finally:
            self.logger.info(f"Information for active {active_name} successfully obtained")

        return ret_stock
