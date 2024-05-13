from typing import List
from astropy import units as u
from dataclasses import dataclass

from .......enum import Shape


@dataclass
class TurbulenceHeatingTimeSeriesReturnModel:
    rKpc: float
    shape: Shape
    rhoIndex: float
    timeMyrList: List[float]
    upperLimit: u.Quantity
    lowerLimit: u.Quantity
    