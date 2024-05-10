from dataclasses import dataclass
from typing import Tuple

from ..data_nd import DataNdCalculationInfoModel

@dataclass(kw_only=True)
class Data3dCalculationInfoModel(DataNdCalculationInfoModel):
    velxFieldName: Tuple[str, str] = ("gas", "velocity_x")
    velyFieldName: Tuple[str, str] = ("gas", "velocity_y")
    velzFieldName: Tuple[str, str] = ("gas", "velocity_z")
    cellCoorField: Tuple[str, str] = ("gas", "x")
    cellCoorUnit: str = "kpc"