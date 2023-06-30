# PyInvestAnalyser

![wakatime](https://wakatime.com/badge/user/541772df-f19f-4145-a40c-cf7ffac73ea5/project/5bfa867f-031e-4498-bdf3-a918ec816f88.svg)

![Python](https://img.shields.io/badge/-Python-3776AB?&logo=Python&logoColor=FFFFFF)
![Docker](https://img.shields.io/badge/-Docker-2496ED?&logo=Docker&logoColor=FFFFFF)
![Pytest](https://img.shields.io/badge/-Pytest-0A9EDC?&logo=Pytest&logoColor=FFFFFF)
![Selenium](https://img.shields.io/badge/-Selenium-43B02A?&logo=Selenium&logoColor=FFFFFF)

[//]: # (![FastAPI]&#40;https://img.shields.io/badge/-FastAPI-009688?&logo=FastAPI&logoColor=FFFFFF&#41;)

[//]: # (![Redis]&#40;https://img.shields.io/badge/-Redis-DC382D?&logo=Redis&logoColor=FFFFFF&#41;)

[//]: # (![Gunicorn]&#40;https://img.shields.io/badge/-Gunicorn-499848?&logo=gunicorn&logoColor=FFFFFF&#41;)


O PyInvestAnalyser é um projeto desenvolvido em Python que utiliza web scraping para obter dados sobre ativos
financeiros. Com o auxílio das bibliotecas Selenium, Docker e Pyenv, você pode analisar informações relevantes sobre
diferentes ativos de forma automatizada.

## Pré-requisitos

Antes de começar, verifique se você possui os seguintes pré-requisitos instalados:

- Python (recomendado usar Pyenv para gerenciamento de pacotes)
- Docker

## Instalação

Siga as etapas abaixo para instalar o projeto:

1. Clone este repositório:

   ```
   $ git clone https://github.com/ericksonlopes/PyInvestAnalyser.git
   ```

2. Acesse o diretório do projeto:

   ```
   $ cd PyInvestAnalyser
   ```

3. Crie e ative um ambiente virtual com o Pyenv:

   ```
   $ pip install pipenv
   $ pipenv install
   ```

4. Instale as dependências do projeto:

   ```
   $ pip install -r requirements.txt
   
   ```
5. Certifique-se de que o Docker esteja em execução.
6. Execute o Docker Compose para iniciar o ambiente de execução:

   ```
   $ docker-compose up -d
   ```

## Uso

Para utilizar o PyInvestAnalyser, siga estas etapas:

Importe a classe ExtractInfoFromStock do respectivo tipo de ativo que você deseja analisar (ações, fundos
imobiliários e DBRs):

Aqui esta um exemplo de como importar a classe ExtractInfoFromStock para obter informações sobre a ação B3SA3:

```python
from src.services import ExtractInfoFromStock

stock = ExtractInfoFromStock().get_info_active('B3SA3')

print(stock)
# Stock(name='B3SA3', company_nam...
```

Além disso, dando contexto a um exemplo mais complexo, você pode executar um script em muilthread para obter informações
de vários ativos ao mesmo tempo:

Neste caso, o script irá obter informações sobre as ações B3SA3, BBDC3, BBSE3 e BMGB4 e salvará os resultados em um
arquivo CSV.

```python
import concurrent.futures
import csv

from src.models import Stock
from src.services import ExtractInfoFromStock

actives = [
    'B3SA3',
    'BBDC3',
    'BBSE3',
    'BMGB4'
]

result_actives = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(ExtractInfoFromStock().get_info_active, active) for active in actives]

    for future in concurrent.futures.as_completed(futures):
        try:
            active = future.result()

            if isinstance(active, str):
                active = ExtractInfoFromStock().get_active_keys_indicators(active)

            result_actives.append(active)

        except Exception as e:
            print(f'Error1: {str(e)}')

with open('result_for_actives.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(Stock().get_meaning_of_fields().values())

    for active in result_actives:
        writer.writerow(active.__dict__.values())
 ```

## Contribuição

Se você deseja contribuir para o projeto PyInvestAnalyser, siga as etapas abaixo:

1. Faça um fork do projeto

2. Crie uma nova branch (git checkout -b feature/nova-feature)

3. Faça suas alterações

4. Faça o commit de suas alterações (git commit -am 'Adicionar nova feature')

5. Faça o push para a branch (git push origin feature/nova-feature)

6. Abra um Pull Request

## Autores

- [Erickson Lopes](<https://www.linkedin.com/in/ericksonlopes/>)

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).

## Referências

- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [Docker](https://www.docker.com/)
- [Pyenv](https://pypi.org/project/pyenv/)
- [Pytest](https://docs.pytest.org/)
- [Investidor10](https://investidor10.com.br)