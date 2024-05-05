from dataclasses import dataclass

from .time_series_calculation_info_model import TimeSeriesCalculationInfoModel
from .....enum import Shape

@dataclass
class TurbulenceHeatingTimeSeriesCalculationInfoModel \
    (TimeSeriesCalculationInfoModel):
    rKpc: float
    tStepMyr: float
    shape: Shape
    rhoIndex: float