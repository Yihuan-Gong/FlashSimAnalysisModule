from dataclasses import dataclass
from astropy import units as u

@dataclass
class SimonteSigmaRhoSigmaVReturnModel:
    sigmaRho: u.Quantity
    sigmaV: u.Quantity