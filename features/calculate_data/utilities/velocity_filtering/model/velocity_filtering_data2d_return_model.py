from dataclasses import dataclass

from ......models.interfaces import (
    VelocityReturnModel,
    Data2dReturnModel
)

@dataclass
class VelocityFilteringData2dReturnModel\
    (VelocityReturnModel, Data2dReturnModel):
    pass
