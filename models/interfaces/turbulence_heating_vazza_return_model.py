from dataclasses import dataclass
from astropy import units as u

@dataclass
class TurbulenceHeatingVazzaReturnModel:
    heating: u.Quantity
    scale: u.Quantity