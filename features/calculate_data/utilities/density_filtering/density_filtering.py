from .models import (
    DensityFilteringCalculationInfoModel,
    DensityFilteringData2dReturnModel,
    DensityFilteringData3dReturnModel
)
from .methods import DensityFilteringMethod
from .....models import SimFileModel


class DensityFiltering:
    __densityFilter: DensityFilteringMethod
    
    
    def setInputs(self, simFile: SimFileModel, calculationInfo: DensityFilteringCalculationInfoModel):
        self.__densityFilter = DensityFilteringMethod()
        self.__densityFilter.setInputs(simFile, calculationInfo)
        return self
    
    
    def getData2d(self, axis: str) -> DensityFilteringData2dReturnModel:
        return self.__densityFilter.getData2d(axis)
    
    
    def getData3d(self) -> DensityFilteringData3dReturnModel:
        return self.__densityFilter.getData3d()