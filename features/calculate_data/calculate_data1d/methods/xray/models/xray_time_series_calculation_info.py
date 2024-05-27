from dataclasses import dataclass
from typing import Tuple

from .interface import XrayCalculationInfo
from ....models.interface import TimeSeriesCalculationInfoModel
from .......enum import Shape

@dataclass(kw_only=True)
class XrayTimeSeriesCalculationInfoModel(
    XrayCalculationInfo,
    TimeSeriesCalculationInfoModel
):
    shape: Shape
    weightFieldName: Tuple[str, str] = ("gas", "mass")
    # radiusFieldName: Tuple[str, str] = ('gas', 'radius')
    # boxRadiusFieldName: Tuple[str, str] = ('gas', 'radius')