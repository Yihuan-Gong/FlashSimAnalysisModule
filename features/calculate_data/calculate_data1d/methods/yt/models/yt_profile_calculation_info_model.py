from dataclasses import dataclass

from .interface import YtCalculationInfo
from ....models.interface import ProfileCalculationInfoModel

@dataclass
class YtProfileCalculationInfoModel(
    YtCalculationInfo,
    ProfileCalculationInfoModel
):
    pass