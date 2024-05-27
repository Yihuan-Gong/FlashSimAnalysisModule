from dataclasses import dataclass
from typing import Tuple

from .interface import XrayCalculationInfo
from ....models.interface import ProfileCalculationInfoModel
from .......enum import Shape

@dataclass(kw_only=True)
class XrayProfileCalculationInfoModel(
    XrayCalculationInfo,
    ProfileCalculationInfoModel
):
    shape: Shape
    weightFieldName: Tuple[str, str] = ("gas", "mass")
    # radiusFieldName: Tuple[str, str] = ('gas', 'radius')
    # boxRadiusFieldName: Tuple[str, str] = ('gas', 'radius')