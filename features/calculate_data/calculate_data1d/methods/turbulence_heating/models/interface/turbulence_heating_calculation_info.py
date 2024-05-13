from dataclasses import dataclass

from ........enum import Shape

@dataclass
class TurbulenceHeatingCalculationInfo:
    rhoIndex: float
    shape: Shape