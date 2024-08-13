from dataclasses import dataclass
from astropy import units as u

from ......models.interfaces import (
    Data3dReturnModel
)


@dataclass
class YtFieldData3dReturnModel\
    (Data3dReturnModel):
    fieldValue: u.Quantity
    radialAvgFieldValue: u.Quantity = None
    radialAvgFilteredFieldValue: u.Quantity = None