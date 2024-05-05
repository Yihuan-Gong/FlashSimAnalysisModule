from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Data1dReturnModel:
    x: List[float]
    value: any
    valueUint: str
    label: Tuple[float, str]