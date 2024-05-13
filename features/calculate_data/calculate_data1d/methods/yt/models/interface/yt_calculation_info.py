from dataclasses import dataclass
from typing import Tuple

from ........enum import Shape

@dataclass
class YtCalculationInfo:
    shape: Shape
    fieldName: Tuple[str, str]
    weightFieldName: Tuple[str, str] = ("gas", "mass") # only needed for GasField.Luminosity