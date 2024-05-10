from dataclasses import dataclass

from ....calculate_data3d.models import Data3dReturnModel
from ......models.interfaces import VelocityReturnModel

@dataclass
class VelocityFilteringData3dReturnModel\
    (Data3dReturnModel, VelocityReturnModel):
    pass
