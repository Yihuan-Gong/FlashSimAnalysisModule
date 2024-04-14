from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class DataModel:
    x: List[float]
    value: any
    label: Tuple[float, str]