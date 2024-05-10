from dataclasses import dataclass

from ..data_nd import DataNdCalculationInfoModel

@dataclass
class Data2dCalculationInfoModel(DataNdCalculationInfoModel):
    axis: str