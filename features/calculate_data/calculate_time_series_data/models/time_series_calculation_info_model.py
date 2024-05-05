from dataclasses import dataclass

from .....enum.shape import Shape

@dataclass
class TimeSeriesCalculationInfoModel:
    tStartMyr: float
    tEndMyr: float

    