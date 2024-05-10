from dataclasses import dataclass

from ......models.interfaces import (
    TurbulenceHeatingVazzaReturnModel,
    Data2dReturnModel
)

@dataclass
class TurbulenceHeatingVazzaData2dReturnModel(
    Data2dReturnModel, 
    TurbulenceHeatingVazzaReturnModel
):
    pass