from dataclasses import dataclass
from typing import List, Tuple

from ....models.interface import ProfileCalculationInfoModel
from .....calculate_data3d import TurbulenceHeatingVazzaCalculationInfoModel
from .......models.interfaces import (
    CoordinateModel, 
    VelocityFieldModel,
)
from .......enum import Shape


@dataclass(kw_only=True)
class TurbulenceHeatingVazzaProfileCalculationInfoModel(
    ProfileCalculationInfoModel,
    CoordinateModel,
    VelocityFieldModel
):
    shape: Shape
    bulkTurbFilteringMinScale: int = 4
    bulkTurbFilteringMaxScale: int = None
    bulkTurbFilteringEps: float = 0.1
    densityFieldName: Tuple[str, str] = ("gas", "density")
    
    
    def toList(self) -> List[TurbulenceHeatingVazzaCalculationInfoModel]:
        calcModelList: List[TurbulenceHeatingVazzaCalculationInfoModel] = []
        for rKpc in self.getRList():
            calcModelList.append(
                TurbulenceHeatingVazzaCalculationInfoModel(
                    timeMyr=self.tMyr,
                    rBoxKpc=rKpc,
                    velxFieldName=self.velxFieldName,
                    velyFieldName=self.velyFieldName,
                    velzFieldName=self.velzFieldName,
                    cellCoorField=self.cellCoorField,
                    cellCoorUnit=self.cellCoorUnit,
                    bulkTurbFilteringEps=self.bulkTurbFilteringEps,
                    bulkTurbFilteringMaxScale=self.bulkTurbFilteringMaxScale,
                    bulkTurbFilteringMinScale=self.bulkTurbFilteringMinScale,
                    densityFieldName=self.densityFieldName
                )
            )
        return calcModelList