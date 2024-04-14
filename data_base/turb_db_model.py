from dataclasses import dataclass

@dataclass
class TurbDbModel:
    rhoIndex: float
    upperLimit: float
    lowerLimit: float