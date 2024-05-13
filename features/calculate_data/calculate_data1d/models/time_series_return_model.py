from typing import List
from astropy import units as u
from dataclasses import dataclass

from .....enum import Shape


@dataclass
class TimeSeriesReturnModel:
    rKpc: float
    shape: Shape
    timeMyrList: List[float]
    yValue: u.Quantity
    