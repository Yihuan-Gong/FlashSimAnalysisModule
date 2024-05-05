from dataclasses import dataclass

from .profile_calculation_info_model import ProfileCalculationInfoModel

@dataclass
class TurbulenceHeatingProfileCalculationInfoModel \
    (ProfileCalculationInfoModel):
    rhoIndex: float