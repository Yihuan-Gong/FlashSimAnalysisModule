from dataclasses import dataclass
from typing import Tuple

from .interface import YtCalculationInfo
from ....models.interface import ProfileCalculationInfoModel

@dataclass
class YtProfileCalculationInfoModel(
    YtCalculationInfo,
    ProfileCalculationInfoModel
):
    radiusFieldName: Tuple[str, str] = ('gas', 'radius')
    pass