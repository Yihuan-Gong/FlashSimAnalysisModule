from dataclasses import dataclass
import astropy.units as u

@dataclass
class VelocityPowerSpectrumInputModel:
    velx: u.Quantity
    vely: u.Quantity
    velz: u.Quantity
    cellSize: u.Quantity
    rbox: u.Quantity
    rhoIndex: float = 0
    rho: u.Quantity = None
