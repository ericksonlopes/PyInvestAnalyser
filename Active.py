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
