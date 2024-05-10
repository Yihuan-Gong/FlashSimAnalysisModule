from dataclasses import dataclass

from ......models.interfaces import (
    VelocityReturnModel, Data3dReturnModel
)


@dataclass
class VelocityFilteringData3dReturnModel\
    (VelocityReturnModel, Data3dReturnModel):
    pass
