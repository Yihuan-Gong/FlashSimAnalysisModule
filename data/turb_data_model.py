from typing import List
from dataclasses import dataclass

@dataclass
class TurbDataModel:
    rhoIndex: float
    upperLimit: List[float]
    lowerLimit: List[float]