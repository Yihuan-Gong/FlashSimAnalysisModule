from dataclasses import dataclass
from astropy import units as u

from ......models.interfaces import (
    Data2dAxisReturnModel
)


@dataclass
class DensityFilteringData2dReturnModel\
    (Data2dAxisReturnModel):
    deltaRho: u.Quantity
    rho: u.Quantity
