from dataclasses import dataclass

from .......models.interfaces import (
    DataNdCalculationInfoModel,
    VelocityFieldModel,
    CoordinateModel
)


@dataclass(kw_only=True)
class LosDispersionCalculationInfoModel(
    DataNdCalculationInfoModel,
    VelocityFieldModel,
    CoordinateModel
):
    pass