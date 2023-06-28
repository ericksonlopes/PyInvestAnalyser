from dataclasses import dataclass
from types import MappingProxyType

from src.models.Active import Active


@dataclass
class Stock(Active):
    p_l: str = None
    p_vp: str = None
    dividend_yield_stock: str = None
    payout: str = None
    net_margin: str = None
    gross_margin: str = None
    ebit_margin: str = None
    ebitda_margin: str = None
    ev_ebitda: str = None
    ev_ebit: str = None
    p_ebitda: str = None
    p_ebit: str = None
    p_assets: str = None
    p_working_capital: str = None
    p_net_current_assets: str = None
    psr: str = None
    vpa: str = None
    lpa: str = None
    asset_turnover: str = None
    roe: str = None
    roic: str = None
    roa: str = None
    net_debt_equity_ratio: str = None
    net_debt_ebitda_ratio: str = None
    net_debt_ebit_ratio: str = None
    gross_debt_equity_ratio: str = None
    equity_assets_ratio: str = None
    liabilities_assets_ratio: str = None
    current_ratio: str = None
    cagr_revenues_5_years: str = None
    cagr_earnings_5_years: str = None

    @classmethod
    def get_meaning_of_fields(cls) -> MappingProxyType:
        active_default = super().get_meaning_of_fields()

        stock = {
            'p_l': 'Preço sobre o Lucro',
            'p_vp': 'Preço sobre o Valor Patrimonial',
            'dividend_yield_stock': 'DIVIDEND YIELD Ação',
            'payout': 'PAYOUT',
            'net_margin': 'MARGEM LÍQUIDA',
            'gross_margin': 'MARGEM BRUTA',
            'ebit_margin': 'MARGEM EBIT',
            'ebitda_margin': 'MARGEM EBITDA',
            'ev_ebitda': 'Valor da Empresa sobre EBITDA',
            'ev_ebit': 'Valor da Empresa sobre EBIT',
            'p_ebitda': 'Preço sobre EBITDA',
            'p_ebit': 'Preço sobre EBIT',
            'p_assets': 'Preço sobre o Ativo Total',
            'p_working_capital': 'Preço sobre o Capital de Giro',
            'p_net_current_assets': 'Preço sobre o Ativo Circulante Líquido',
            'psr': 'PSR - PREÇO SOBRE RECEITA LÍQUIDA',
            'vpa': 'VPA - VALOR PATRIMONIAL POR AÇÃO',
            'lpa': 'LPA - LUCRO POR AÇÃO',
            'asset_turnover': 'GIRO ATIVOS',
            'roe': 'ROE - RETORNO SOBRE PATRIMÔNIO LÍQUIDO',
            'roic': 'ROIC - RETORNO SOBRE CAPITAL INVESTIDO',
            'roa': 'ROA - RETORNO SOBRE ATIVO',
            'net_debt_equity_ratio': 'DÍVIDA LÍQUIDA / PATRIMÔNIO',
            'net_debt_ebitda_ratio': 'DÍVIDA LÍQUIDA / EBITDA',
            'net_debt_ebit_ratio': 'DÍVIDA LÍQUIDA / EBIT',
            'gross_debt_equity_ratio': 'DÍVIDA BRUTA / PATRIMÔNIO',
            'equity_assets_ratio': 'PATRIMÔNIO / ATIVOS',
            'liabilities_assets_ratio': 'PASSIVOS / ATIVOS',
            'current_ratio': 'LIQUIDEZ CORRENTE',
            'cagr_revenues_5_years': 'Crescimento anual composta 5 Anos',
            'cagr_earnings_5_years': 'Crescimento anual composta 5 Anos'
        }

        return MappingProxyType(dict(active_default, **stock))
