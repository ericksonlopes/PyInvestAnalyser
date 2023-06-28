from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import Logger
from src.exceptions import ActiveSearchError
from src.helpers import get_webdriver
from src.models import Active


class ExtractActiveInformation(ABC, Logger):
    def __init__(self):
        super().__init__()
        self.soup = None

    @abstractmethod
    def get_active_keys_indicators(self, active_name) -> dict:
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

    def get_indicators(self) -> dict:
        indicators = {}

        table_indicators = self.soup.find('div', id='table-indicators').find_all("div", class_="cell")

        for cell in table_indicators:
            indicator = cell.span.text.replace("\n", "")

            value = self.get_value_cell(cell)

            indicators[indicator] = value

        return indicators

    def get_page_infos_for_active(self, active_name, active_type, time_for_loop=0) -> dict:
        self.logger.info(f"Getting information {active_name}... {time_for_loop if time_for_loop > 0 else ''}")

        driver = get_webdriver()
        active = Active(name=active_name, type=active_type)

        try:
            if time_for_loop == 5:
                raise ActiveSearchError(f"Error to get information for active {active_name}")

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

            company_name = soup.find(class_='name-ticker').find("h2")
            active.company_name = company_name.text

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

        except ActiveSearchError as error:
            driver.quit()
            self.logger.error(f"Maximum attempts to get information for active {active_name} {error}")
            return active_name

        except Exception as error:
            driver.quit()
            self.logger.error(f"Error to get information for active {active_name} {error}")
            return self.get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

        if "-" in active.quotation:
            driver.quit()
            self.logger.warning(f"Error to get information for active {active_name} '-' quotation is not available")
            return self.get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

        driver.quit()
        self.logger.info(f"Information for active {active_name} successfully obtained")
        return {**active.__dict__, **indicators}
