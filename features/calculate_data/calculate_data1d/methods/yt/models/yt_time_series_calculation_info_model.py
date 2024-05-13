from dataclasses import dataclass

from .interface import YtCalculationInfo
from ....models.interface import TimeSeriesCalculationInfoModel

@dataclass(kw_only=False)
class YtTimeSeriesCalculationInfoModel(
    YtCalculationInfo,
    TimeSeriesCalculationInfoModel
):
    pass