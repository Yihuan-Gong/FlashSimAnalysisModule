from dataclasses import dataclass

from ....calculate_data2d.models import Data2dReturnModel
from ......models.interfaces import VelocityReturnModel

@dataclass
class VelocityFilteringData2dReturnModel\
    (Data2dReturnModel, VelocityReturnModel):
    pass
