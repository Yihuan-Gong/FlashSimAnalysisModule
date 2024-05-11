from dataclasses import dataclass
from astropy import units as u

@dataclass
class TurbulenceHeatingVazzaReturnModel:
    heatingPerVolume: u.Quantity
    heatingPerMass: u.Quantity
    scale: u.Quantity