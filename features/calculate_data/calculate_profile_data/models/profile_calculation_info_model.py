from dataclasses import dataclass

from .....enum import Shape

@dataclass
class ProfileCalculationInfoModel:
    rStartKpc: float
    rEndKpc: float
    rStepKpc: float
    shape: Shape
    tMyr: float

