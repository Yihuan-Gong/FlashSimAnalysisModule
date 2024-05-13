from dataclasses import dataclass

from ..models.interface import TurbulenceHeatingCalculationInfo
from ....models.interface import ProfileCalculationInfoModel


@dataclass
class TurbulenceHeatingProfileCalculationInfoModel(
    ProfileCalculationInfoModel,
    TurbulenceHeatingCalculationInfo
):
    pass
    