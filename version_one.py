import concurrent.futures
import csv
import os
import platform
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

from Active import Active


def download_webdriver():
    # gets the current operating system
    system = platform.system()

    # Directory where the webdriver will be stored
    webdriver_dir = os.path.join(os.getcwd(), 'webdriver')

    # Checks the operating system and sets the appropriate driver URL and name
    if system == 'Windows':
        driver_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        driver_name = 'chromedriver_win32.zip'
    elif system == 'Linux':
        driver_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        driver_name = 'chromedriver_linux64.zip'
    else:
        print(f'Não há suporte para o sistema operacional {system}.')
        return

    # Create the webdriver directory if it doesn't exist
    os.makedirs(webdriver_dir, exist_ok=True)

    # Creates a .gitignore file inside the webdriver directory so that it will be ignored by version control (Git)
    print("*", file=open(os.path.join(webdriver_dir, ".gitignore"), 'w', encoding='utf-8'))

    # Full path to webdriver
    webdriver_path = os.path.join(webdriver_dir, driver_name)

    # Checks if the webdriver has already been downloaded
    if not os.path.exists(webdriver_path):
        try:
            import requests
            # Get the latest version of the webdriver
            response = requests.get(driver_url)
            version = response.text.strip()
            # Constructs the webdriver download URL
            driver_url = f'https://chromedriver.storage.googleapis.com/{version}/{driver_name}'
            response = requests.get(driver_url)
            # Save the webdriver file to disk
            with open(webdriver_path, 'wb') as file:
                file.write(response.content)
            print(f'Webdriver baixado com sucesso para {system}.')
        except Exception as e:
            print(f'Falha ao baixar o webdriver: {str(e)}')
    else:
        print(f'O webdriver para {system} já existe.')

    return webdriver_path


def get_page_infos_for_active(active_name, active_type, time_for_loop=0):
    print(f"getting information {active_name}... {time_for_loop if time_for_loop > 0 else ''}")

    path_webdriver = download_webdriver()

    if not path_webdriver:
        exit()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    try:
        active = Active(name=active_name, type=active_type)

        if time_for_loop > 10:
            return active.__dict__

        url = f"https://investidor10.com.br/{active_type}/{active_name}/"
        # Acessando o site
        driver.get(url)
        driver.execute_script("$.fn.dataTable.ext.errMode = 'throw';")

        sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

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

        if active_type == "acoes":
            grade = soup.find('div', id="checklist").find('div', class_='rating')
            grade_text = grade.text.replace("\n", "").replace(" ", "").replace("Nota", "").replace(":", "")
            active.grade = grade_text
        else:
            active.grade = "-"

    except Exception:
        driver.quit()
        return get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

    if "-" in active.quotation:
        return get_page_infos_for_active(active_name, active_type, time_for_loop + 1)

    driver.quit()

    return active.__dict__


def main():
    print("Starting...")

    actives = [
        {"active": 'AAPL34', "type": "bdrs"},
        {"active": 'B3SA3', "type": "acoes"},
        {"active": 'BBDC3', "type": "acoes"},
        {"active": 'BBSE3', "type": "acoes"},
        {"active": 'BIME11', "type": "fiis"},
        {"active": 'MXRF11', "type": "fiis"},
        {"active": 'SNAG11', "type": "fiis"},
        {"active": 'BMGB4', "type": "acoes"},
    ]

    result_actives = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_page_infos_for_active, active["active"], active["type"], 0) for active in
                   actives]

        for future in concurrent.futures.as_completed(futures):
            try:
                active = future.result()
                print(active)
                result_actives.append(active)

            except Exception as e:
                print(f'Error1: {str(e)}')

    with open('result_actives.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(Active().__dict__.keys())

        for active in result_actives:
            writer.writerow(active.values())

    print("FINISHED")


if __name__ == '__main__':
    main()
