from .strategies import *
from .model import (
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from .enums import VelocityFilteringMode
from .....models import SimFileModel

class VelocityFiltering:
    __strategy: VelocityFilteringStrategy
    
    
    def setInputs(self, mode: VelocityFilteringMode, simFile: SimFileModel, 
                  calculationInfo: VelocityFilteringCalculationInfoModel):
        className: str = f"{mode}".split(".")[-1] + VelocityFilteringStrategy.__name__
        self.__strategy = globals()[className]()
        self.__strategy.setInputs(simFile, calculationInfo)
        return self
    
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        return self.__strategy.getData3d()
    
    
    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        return self.__strategy.getData2d(axis)
        