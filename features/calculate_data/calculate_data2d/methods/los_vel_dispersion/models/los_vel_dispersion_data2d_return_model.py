from dataclasses import dataclass
from astropy import units as u

from .......models.interfaces import Data2dAxisReturnModel

@dataclass
class LosVelDispersionData2dReturnModel(
    Data2dAxisReturnModel
):
    value: u.Quantity


