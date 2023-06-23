from dataclasses import dataclass

from src.models.Active import Active


@dataclass
class BDR(Active):
    p_l: float = None
    p_vp: float = None
    p_e: float = None
    dividend_yield: float = None
    roa: float = None
    roe: float = None
    roic: float = None
    net_margin: float = None
    gross_margin: float = None
    operating_margin: float = None
    p_ebit: float = None
    p_ebitda: float = None
    p_assets: float = None
    vpa: float = None
    lpa: float = None
    equity_assets_ratio: float = None
    liabilities_assets_ratio: float = None
    cagr_revenues_5_years: float = None
    cagr_earnings_5_years: float = None

    @staticmethod
    def get_meaning_of_fields() -> dict:
        return {
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
