from typing import Tuple
from dataclasses import dataclass

from .profile_calculation_info_model import ProfileCalculationInfoModel
from .....enum import GasField

@dataclass
class GasPropertyProfileCalculationInfoModel \
    (ProfileCalculationInfoModel):
    gasProperty: GasField
    isLogR: bool = False
    weightFieldName: Tuple[str, str] = ("gas", "mass")