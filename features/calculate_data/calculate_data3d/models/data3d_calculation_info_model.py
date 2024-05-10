from dataclasses import dataclass
from typing import Tuple

from .....models.data_nd_model.data_nd_calculation_info_model import DataNdCalculationInfoModel

@dataclass(kw_only=True)
class Data3dCalculationInfoModel(DataNdCalculationInfoModel):
    velxFieldName: Tuple[str, str] = ("gas", "velocity_x")
    velyFieldName: Tuple[str, str] = ("gas", "velocity_y")
    velzFieldName: Tuple[str, str] = ("gas", "velocity_z")
    cellCoorField: Tuple[str, str] = ("gas", "x")
    cellCoorUnit: str = "kpc"