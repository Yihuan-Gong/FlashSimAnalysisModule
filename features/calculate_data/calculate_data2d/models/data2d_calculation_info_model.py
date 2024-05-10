from dataclasses import dataclass

from .....models.data_nd_model.data_nd_calculation_info_model import DataNdCalculationInfoModel

@dataclass
class Data2dCalculationInfoModel(DataNdCalculationInfoModel):
    axis: str