from dataclasses import dataclass
from astropy import units as u
import numpy as np

@dataclass
class VelocityReturnModel:
    Vx: u.Quantity = None
    Vy: u.Quantity = None
    Vz: u.Quantity = None
    Vtotal: u.Quantity = None
    turbVx: u.Quantity = None
    turbVy: u.Quantity = None
    turbVz: u.Quantity = None
    turbVtotal: u.Quantity = None
    scaleCells: np.ndarray = None
    scale: u.Quantity = None
    compVx: u.Quantity = None
    compVy: u.Quantity = None
    compVz: u.Quantity = None
    compVtotal: u.Quantity = None
    soleVx: u.Quantity = None
    soleVy: u.Quantity = None
    soleVz: u.Quantity = None
    soleVtotal: u.Quantity = None
    turbCompVx: u.Quantity = None
    turbCompVy: u.Quantity = None
    turbCompVz: u.Quantity = None
    turbCompVtotal: u.Quantity = None
    turbSoleVx: u.Quantity = None
    turbSoleVy: u.Quantity = None
    turbSoleVz: u.Quantity = None
    turbSoleVtotal: u.Quantity = None
    simonteVtotal: u.Quantity = None
