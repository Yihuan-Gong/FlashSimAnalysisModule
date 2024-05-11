from dataclasses import dataclass

from ......models.interfaces import (
    VelocityReturnModel,
    Data2dAxisReturnModel
)

@dataclass
class VelocityFilteringData2dReturnModel\
    (VelocityReturnModel, Data2dAxisReturnModel):
    pass
