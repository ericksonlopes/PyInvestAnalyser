from dataclasses import dataclass
from types import MappingProxyType

from src.models.Active import Active


@dataclass
class BDR(Active):
    p_l: str = None
    p_vp: str = None
    p_e: str = None
    dividend_yield: str = None
    roa: str = None
    roe: str = None
    roic: str = None
    net_margin: str = None
    gross_margin: str = None
    operating_margin: str = None
    p_ebit: str = None
    p_ebitda: str = None
    p_assets: str = None
    vpa: str = None
    lpa: str = None
    equity_assets_ratio: str = None
    liabilities_assets_ratio: str = None
    cagr_revenues_5_years: str = None
    cagr_earnings_5_years: str = None

    @classmethod
    def get_meaning_of_fields(cls) -> MappingProxyType:
        active_default = super().get_meaning_of_fields()

        bdr = {
            'p_l': 'P/L Preço sobre o Lucro',
            'p_vp': 'P/VP Preço sobre o Valor Patrimonial',
            'p_e': 'P/E = Índice Preço Lucro',
            'dividend_yield_dy': 'Dividend Yield (DY)',
            'roa': 'ROA = Retorno sobre o Ativo',
            'roe': 'ROE = Retorno sobre Patrimônio Líquido',
            'roic': 'ROIC = Retorno sobre o Capital Investido',
            'net_margin': 'Margem Líquida',
            'gross_margin': 'Margem Bruta',
            'operating_margin': 'Margem Operacional',
            'p_ebit': 'Preço sobre EBIT',
            'p_ebitda': 'Preço sobre EBITDA',
            'p_assets': 'P/ATIVO = Preço sobre Total de Ativos',
            'vpa': 'VPA - Valor Patrimonial por Ação',
            'lpa': 'LPA - Lucro por Ação',
            'equity_assets_ratio': 'Patrimônio/Ativos',
            'liabilities_assets_ratio': 'Passivos/Ativos',
            'cagr_revenues_5_years': 'Crescimento anual composta 5 Anos',
            'cagr_earnings_5_years': 'Crescimento anual composta 5 Anos',
        }

        return MappingProxyType(dict(**active_default, **bdr))
