from typing import Tuple
from dataclasses import dataclass

from .time_series_calculation_info_model import TimeSeriesCalculationInfoModel
from .....enum import GasField, Shape

@dataclass
class GasPropertyTimeSeriesCalculationInfoModel \
    (TimeSeriesCalculationInfoModel):
    rKpc: float
    tStepMyr: float
    shape: Shape
    gasProperty: GasField
    weightFieldName: Tuple[str, str] = ("gas", "mass") # only needed for GasField.Luminosity