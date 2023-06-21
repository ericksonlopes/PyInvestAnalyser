import concurrent.futures
import os
import platform
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Active import Active


def download_webdriver():
    # Obtém o sistema operacional atual
    system = platform.system()

    # Diretório onde o webdriver será armazenado
    webdriver_dir = os.path.join(os.getcwd(), 'webdriver')

    # Verifica o sistema operacional e define o URL e o nome do driver apropriado
    if system == 'Windows':
        driver_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        driver_name = 'chromedriver_win32.zip'
    elif system == 'Linux':
        driver_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        driver_name = 'chromedriver_linux64.zip'
    else:
        print(f'Não há suporte para o sistema operacional {system}.')
        return

    # Cria o diretório do webdriver, se não existir
    os.makedirs(webdriver_dir, exist_ok=True)

    # Cria um arquivo .gitignore dentro do diretório do webdriver
    # para que ele seja ignorado pelo controle de versão (Git)
    print("*", file=open(os.path.join(webdriver_dir, ".gitignore"), 'w', encoding='utf-8'))

    # Caminho completo para o webdriver
    webdriver_path = os.path.join(webdriver_dir, driver_name)

    # Verifica se o webdriver já foi baixado
    if not os.path.exists(webdriver_path):
        try:
            import requests
            # Obtém a versão mais recente do webdriver
            response = requests.get(driver_url)
            version = response.text.strip()
            # Constrói o URL de download do webdriver
            driver_url = f'https://chromedriver.storage.googleapis.com/{version}/{driver_name}'
            response = requests.get(driver_url)
            # Salva o arquivo do webdriver no disco
            with open(webdriver_path, 'wb') as file:
                file.write(response.content)
            print(f'Webdriver baixado com sucesso para {system}.')
        except Exception as e:
            print(f'Falha ao baixar o webdriver: {str(e)}')
    else:
        # print(f'O webdriver para {system} já existe.')
        pass

    return webdriver_path


def get_page_infos_for_active(active_name, active_type, ):
    active = Active()
    active.name = active_name
    active.type = active_type

    print(f"getting information {active_name}...")

    # Função para fazer o download do webdriver e retornar o caminho do arquivo
    path_webdriver = download_webdriver()

    # Verifica se o webdriver foi baixado corretamente
    if not path_webdriver:
        exit()

    # Configuração do driver do Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Execução sem abrir a janela do navegador
    options.add_argument('--no-sandbox')

    # Inicializa o driver do Selenium usando o caminho do webdriver
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://investidor10.com.br/{active_type}/{active_name}/"
        # Acessando o site
        driver.get(url)
        driver.execute_script("$.fn.dataTable.ext.errMode = 'throw';")

        try:
            alert = Alert(driver)

            alert_text = alert.text
            print('Texto do alerta:', alert_text)

            # Fechando o alerta
            alert.dismiss()
        except Exception:
            pass

        try:
            quotation = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_card.cotacao")))
            if quotation.text == "-":
                return get_page_infos_for_active(active_name, active_type)
        except Exception:
            print("Não foi possível obter a cotação")

        sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            quotation = soup.find('div', class_='_card cotacao').find("div", class_="_card-body").find("span")
            active.quotation = quotation.text

        except Exception:
            print("Não foi possível obter a cotação")

        try:
            dividend_yield = soup.find('div', class_='_card dy').find("div", class_="_card-body").find("span")
            active.dividend_yield = dividend_yield.text
        except Exception:
            print("Não foi possível obter o dividend yield")

        try:
            price_to_book_ratio = soup.find('div', class_='_card vp').find("div", class_="_card-body").find("span")
            active.price_to_book_ratio = price_to_book_ratio.text
        except Exception:
            print("Não foi possível obter o price to book ratio")

        try:
            daily_liquidity = soup.find('div', class_='_card val').find("div", class_="_card-body").find("span")
            daily_liquidity = daily_liquidity.text.replace("R$ ", "").replace(" K", "")
            active.daily_liquidity = daily_liquidity
        except Exception:
            print("Não foi possível obter a liquidez diária")

        try:
            appreciation = soup.find('div', class_='_card dy').find("div", class_="_card-body").find("span")
            active.appreciation = appreciation.text
        except Exception:
            print("Não foi possível obter a valorização")

        if active_type == "acoes":
            try:
                grade = soup.find('div', id="checklist").find('div', class_='rating')
                grade_text = grade.text.replace("\n", "").replace(" ", "").replace("Nota", "").replace(":", "")
                active.grade = grade_text
            except Exception as e:
                print(f"Não foi possível obter a nota {e}")

    except Exception as e:
        print(e)
        driver.quit()
        return None

    finally:
        # Fechando o driver do Selenium
        driver.quit()
        return active.__dict__


def main():
    # URLs dos sites
    actives = [
        {"active": 'AAPL34', "type": "bdrs"},
        {"active": 'B3SA3', "type": "acoes"},
        {"active": 'BBDC3', "type": "acoes"},
        {"active": 'BBSE3', "type": "acoes"},
        {"active": 'BIME11', "type": "fiis"},
        {"active": 'SNAG11', "type": "fiis"},
        {"active": 'BMGB4', "type": "acoes"},
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_page_infos_for_active, active["active"], active["type"]) for active in actives]

        for future in concurrent.futures.as_completed(futures):
            try:
                active = future.result()
                print(f'Info active: {active}')
            except Exception as e:
                print(f'Error: {str(e)}')


if __name__ == '__main__':
    main()
