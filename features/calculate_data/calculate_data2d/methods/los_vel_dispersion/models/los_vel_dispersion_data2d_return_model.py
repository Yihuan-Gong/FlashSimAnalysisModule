from dataclasses import dataclass
from astropy import units as u

from .......models.interfaces import Data2dReturnModel

@dataclass
class LosVelDispersionData2dReturnModel(
    Data2dReturnModel
):
    value: u.Quantity


