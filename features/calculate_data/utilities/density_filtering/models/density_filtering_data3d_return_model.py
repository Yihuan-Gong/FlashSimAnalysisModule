from dataclasses import dataclass
from astropy import units as u

from ......models.interfaces import (
    Data3dReturnModel
)


@dataclass
class DensityFilteringData3dReturnModel\
    (Data3dReturnModel):
    deltaRho: u.Quantity
    rho: u.Quantity
