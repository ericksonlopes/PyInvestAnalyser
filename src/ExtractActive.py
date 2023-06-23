from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings import get_webdriver
from src.exceptions import ActiveSearchError
from src.models import Active, Stock, RealEstateFunds, BDR


class ExtractActiveInformation(ABC):
    def __init__(self):
        self.soup = None

    @abstractmethod
    def get_active_keys_indicators(self, active_name, active_type) -> dict:
        pass

    @abstractmethod
    def get_value_cell(self, cell: Tag):
        pass

    @abstractmethod
    def get_info_active(self, active_name: str):
        pass

    @abstractmethod
    def get_grade(self):
        pass

    @classmethod
    def webdriver(cls):
        return get_webdriver()

    def get_indicators(self) -> dict:
        indicators = {}

        table_indicators = self.soup.find('div', id='table-indicators').find_all("div", class_="cell")

        for cell in table_indicators:
            indicator = cell.span.text.replace("\n", "")

            value = self.get_value_cell(cell)

            indicators[indicator] = value

        return indicators

    def get_page_infos_for_active(self, active_name, active_type, time_for_loop=0) -> dict:
        print(f"Getting information {active_name}... {time_for_loop if time_for_loop > 0 else ''}")

        driver = get_webdriver()
        active = Active(name=active_name, type=active_type)

        try:
            if time_for_loop > 5:
                raise ActiveSearchError("Error to get information for active")

            url = f"https://investidor10.com.br/{active_type}/{active_name}/"

            driver.get(url)

            try:
                wait = WebDriverWait(driver, 3)
                alert = wait.until(EC.alert_is_present())
                alert.accept()
            except Exception:
                pass

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            self.soup = soup

            quotation = soup.find('div', class_='_card cotacao').find("div", class_="_card-body").find("span")
            active.quotation = quotation.text

            dividend_yield = soup.find('div', class_='_card dy').find("div", class_="_card-body").find("span")
            active.dividend_yield = dividend_yield.text

            price_to_book_ratio = soup.find('div', class_='_card vp').find("div", class_="_card-body").find("span")
            active.price_to_book_ratio = price_to_book_ratio.text

            daily_liquidity = soup.find('div', class_='_card val').find("div", class_="_card-body").find("span")
            daily_liquidity = daily_liquidity.text.replace("R$ ", "").replace(" K", "")
            active.daily_liquidity = daily_liquidity

            appreciation = soup.find('div', class_='_card dy').find("div", class_="_card-body").find("span")
            active.appreciation = appreciation.text

            active.grade = self.get_grade()

            indicators = self.get_indicators()

        except ActiveSearchError:
            driver.quit()
            return self.get_active_keys_indicators(active_name, active_type)

        except Exception:
            driver.quit()
            return self.get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

        if "-" in active.quotation:
            return self.get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

        driver.quit()
        return {**active.__dict__, **indicators}


class ExtractInfoFromBDR(ExtractActiveInformation):
    def __init__(self):
        super().__init__()

    def get_grade(self):
        return "-"

    def get_value_cell(self, cell: Tag):
        return cell.div.text.replace("\n", "")

    def get_active_keys_indicators(self, active_name, active_type) -> dict:
        return BDR(name=active_name, type=active_type).__dict__

    def get_info_active(self, active_name: str) -> BDR:
        bdr = self.get_page_infos_for_active(active_name, "bdrs")

        ret_bdr = BDR()
        list_bdr_keys = list(BDR().__dict__.keys())

        for num in range(len(list_bdr_keys)):
            ret_bdr.__dict__[list_bdr_keys[num]] = list(bdr.values())[num]

        return ret_bdr


class ExtractInfoFromREF(ExtractActiveInformation):
    def __init__(self):
        super().__init__()

    def get_grade(self):
        return "-"

    def get_value_cell(self, cell: Tag) -> str:
        return cell.find("div", class_="value").text.replace("\n", "")

    def get_active_keys_indicators(self, active_name, active_type) -> dict:
        return RealEstateFunds(name=active_name, type=active_type).__dict__

    def get_info_active(self, active_name: str) -> RealEstateFunds:
        ref = self.get_page_infos_for_active(active_name, "fiis")

        ret_ref = RealEstateFunds()
        list_keys_ref = list(RealEstateFunds().__dict__.keys())

        for num in range(len(list_keys_ref)):
            ret_ref.__dict__[list_keys_ref[num]] = list(ref.values())[num]

        return ret_ref


class ExtractInfoFromStock(ExtractActiveInformation):
    def __init__(self):
        super().__init__()

    def get_value_cell(self, cell: Tag):
        return cell.div.text.replace("\n", "")

    def get_active_keys_indicators(self, active_name, active_type) -> dict:
        return Stock(name=active_name, type=active_type).__dict__

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
