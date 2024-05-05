from typing import List
from dataclasses import dataclass

@dataclass
class TurbDataReturnModel:
    rhoIndex: float
    upperLimit: List[float]
    lowerLimit: List[float]