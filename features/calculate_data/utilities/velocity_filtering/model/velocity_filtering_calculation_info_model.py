from dataclasses import dataclass
from typing import Tuple

from ......models.interfaces import (
    CoordinateModel, 
    VelocityFieldModel,
    DataNdCalculationInfoModel
)

@dataclass(kw_only=True)
class VelocityFilteringCalculationInfoModel \
    (DataNdCalculationInfoModel, CoordinateModel, VelocityFieldModel):
    bulkTurbFilteringMinScale: int = 4
    bulkTurbFilteringMaxScale: int = None
    bulkTurbFilteringEps: float = 0.1
    densityFieldName: Tuple[str, str] = ("gas", "density")
    pass
