from dataclasses import dataclass
from types import MappingProxyType

from src.models.Active import Active


@dataclass
class RealEstateFunds(Active):
    company_name: str = None
    cnpj: str = None
    target_audience: str = None
    mandate: str = None
    segment: str = None
    fund_type: str = None
    duration: str = None
    management_type: str = None
    administration_fee: float = None
    vacancy: float = None
    number_of_investors: int = None
    issued_shares: int = None
    net_asset_value_per_share: float = None
    net_asset_value: float = None
    last_yield: float = None

    @classmethod
    def get_meaning_of_fields(cls) -> MappingProxyType:
        active_default = super().get_meaning_of_fields()

        ref = {
            "company_name": "Razão Social",
            "cnpj": "CNPJ",
            "target_audience": "PÚBLICO - ALVO",
            "mandate": "MANDATO",
            "segment": "SEGMENTO",
            "fund_type": "TIPO DE FUNDO",
            "duration": "PRAZO DE DURAÇÃO",
            "management_type": "TIPO DE GESTÃO",
            "administration_fee": "TAXA DE ADMINISTRAÇÃO",
            "vacancy": "VACÂNCIA",
            "number_of_investors": "NUMERO DE COTISTAS",
            "issued_shares": "COTAS EMITIDAS",
            "net_asset_value_per_share": "VAL.PATRIMONIAL P / COTA",
            "net_asset_value": "VALOR PATRIMONIAL",
            "last_yield": "ÚLTIMO RENDIMENTO"
        }

        return MappingProxyType(dict(**active_default, **ref))
