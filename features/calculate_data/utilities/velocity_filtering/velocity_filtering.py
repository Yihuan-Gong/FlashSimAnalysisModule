from typing import Dict
from .strategies import *
from .model import (
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from .enums import VelocityFilteringMode, VelocityFilteringField
from .....models import SimFileModel

class VelocityFiltering:
    __strategy: VelocityFilteringStrategy
    __fieldToMode: Dict[VelocityFilteringField, VelocityFilteringMode]
    
    def __init__(self) -> None:
        self.__fieldToMode = {
            VelocityFilteringField.Vtotal : VelocityFilteringMode.Total,
            VelocityFilteringField.turbVtotal : VelocityFilteringMode.BulkTurb,
            VelocityFilteringField.scale : VelocityFilteringMode.BulkTurb,
            VelocityFilteringField.compVtotal : VelocityFilteringMode.CompSole,
            VelocityFilteringField.soleVtotal : VelocityFilteringMode.CompSole,
            VelocityFilteringField.turbCompVtotal : VelocityFilteringMode.TurbCompSole,
            VelocityFilteringField.turbSoleVtotal : VelocityFilteringMode.TurbCompSole,
            VelocityFilteringField.simonteVtotal : VelocityFilteringMode.Simonte
        } 
    
    
    def setInputs(self, mode: VelocityFilteringMode, simFile: SimFileModel, 
                  calculationInfo: VelocityFilteringCalculationInfoModel):
        className: str = f"{mode}".split(".")[-1] + VelocityFilteringStrategy.__name__
        self.__strategy = globals()[className]()
        self.__strategy.setInputs(simFile, calculationInfo)
        return self
    
    
    def setInputsByField(self, field: VelocityFilteringField, simFile: SimFileModel, 
        calculationInfo: VelocityFilteringCalculationInfoModel):
        self.setInputs(self.__fieldToMode[field], simFile, calculationInfo)
        return self
    
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        return self.__strategy.getData3d()
    
    
    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        return self.__strategy.getData2d(axis)
        