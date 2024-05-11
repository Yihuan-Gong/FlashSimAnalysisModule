from dataclasses import dataclass

from ......models.interfaces import (
    TurbulenceHeatingVazzaReturnModel,
    Data2dAxisReturnModel
)

@dataclass
class TurbulenceHeatingVazzaData2dReturnModel(
    Data2dAxisReturnModel, 
    TurbulenceHeatingVazzaReturnModel
):
    pass