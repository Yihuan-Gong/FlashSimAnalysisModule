from dataclasses import dataclass
from typing import Tuple

from ...velocity_filtering import VelocityFilteringCalculationInfoModel

@dataclass(kw_only=True)
class TurbulenceHeatingVazzaCalculationInfoModel(
    VelocityFilteringCalculationInfoModel
):
    densityFieldName: Tuple[str, str] = ("gas", "density")