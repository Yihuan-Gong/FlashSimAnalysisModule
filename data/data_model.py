from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class DataModel:
    x: List[float]
    value: List[float]
    label: Tuple[float, str]