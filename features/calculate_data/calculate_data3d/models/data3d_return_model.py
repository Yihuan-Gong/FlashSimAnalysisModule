from dataclasses import dataclass
from astropy import units as u
from typing import Dict

@dataclass
class Data3dReturnModel:
    xAxis: u.Quantity
    yAxis: u.Quantity
    zAxis: u.Quantity
