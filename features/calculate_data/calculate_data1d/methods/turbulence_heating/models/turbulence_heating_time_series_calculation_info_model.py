from dataclasses import dataclass

from ..models.interface import TurbulenceHeatingCalculationInfo
from ....models.interface import TimeSeriesCalculationInfoModel


@dataclass
class TurbulenceHeatingTimeSeriesCalculationInfoModel(
    TurbulenceHeatingCalculationInfo,
    TimeSeriesCalculationInfoModel
):
    pass
    