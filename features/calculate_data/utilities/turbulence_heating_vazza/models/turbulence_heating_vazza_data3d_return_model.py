from dataclasses import dataclass

from ......models.interfaces import (
    Data3dReturnModel,
    TurbulenceHeatingVazzaReturnModel
)

@dataclass
class TurbulenceHeatingVazzaData3dReturnModel(
    Data3dReturnModel, 
    TurbulenceHeatingVazzaReturnModel
):
    pass