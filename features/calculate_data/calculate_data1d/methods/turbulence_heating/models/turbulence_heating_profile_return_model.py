from typing import List
from astropy import units as u
from dataclasses import dataclass

from .......enum import Shape


@dataclass
class TurbulenceHeatingProfileReturnModel:
    timeMyr: float
    shape: Shape
    rhoIndex: float
    rKpcList: List[float]
    upperLimit: u.Quantity
    lowerLimit: u.Quantity
    
    