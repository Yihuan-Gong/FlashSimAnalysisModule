from typing import List
from astropy import units as u
from dataclasses import dataclass

from .....enum import Shape


@dataclass
class ProfileReturnModel:
    timeMyr: float
    shape: Shape
    rKpcList: List[float]
    yValue: u.Quantity
    
    