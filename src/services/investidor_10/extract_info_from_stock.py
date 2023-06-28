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
        stock = self.get_page_infos_for_active(active_name, "acoes")

        ret_stock = Stock()
        list_keys_stock = list(Stock().__dict__.keys())

        for num in range(len(list_keys_stock)):
            ret_stock.__dict__[list_keys_stock[num]] = list(stock.values())[num]

        return ret_stock
