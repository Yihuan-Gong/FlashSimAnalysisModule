from astropy import units as u
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Data2dReturnModel:
    horizontalAxis: Tuple[str, u.Quantity]
    verticalAxis: Tuple[str, u.Quantity]