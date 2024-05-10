from dataclasses import dataclass

from ......models import DataNdCalculationInfoModel
from ......models.interfaces import CoordinateModel, VelocityFieldModel

@dataclass(kw_only=True)
class VelocityFilteringCalculationInfoModel \
    (DataNdCalculationInfoModel, CoordinateModel, VelocityFieldModel):
    bulkTurbFilteringMinScale: int = 4
    bulkTurbFilteringMaxScale: int = None
    bulkTurbFilteringEps: float = 0.1
    pass
