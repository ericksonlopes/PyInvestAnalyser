from dataclasses import dataclass


@dataclass
class Active:
    name: str = None
    type: str = None
    quotation: str = None
    price_to_book_ratio: str = None
    daily_liquidity: str = None
    dividend_yield: str = None
    appreciation: str = None
    grade: str = None

    @staticmethod
    def get_meaning_of_fields():
        return {
            'name': 'Nome',
            'type': 'Tipo',
            'quotation': 'Cotação',
            'price_to_book_ratio': 'P/VP - Preço sobre o Valor Patrimonial',
            'daily_liquidity': 'Liquidez Diária',
            'dividend_yield': 'Dividend Yield',
            'appreciation': 'Valorização',
            'grade': 'Classificação'
        }
