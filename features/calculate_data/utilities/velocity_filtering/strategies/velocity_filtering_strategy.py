import yt
from abc import ABC, abstractmethod

from ..model import (
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from ......models import SimFileModel
from ......services import PickleService

class VelocityFilteringStrategy(ABC):
    _simFile: SimFileModel
    _calculationInfo: VelocityFilteringCalculationInfoModel
    _cube: yt.data_objects.construction_data_containers.YTCoveringGrid
    _cubeDims: int
    _pickleService: PickleService
    
    def setInputs(self, simFile: SimFileModel, calculationInfo: VelocityFilteringCalculationInfoModel):
        self._simFile = simFile
        self._calculationInfo = calculationInfo
        self._pickleService = PickleService(
            simPath=simFile.simPath,
            prefix=self.__class__.__name__,
            timeMyr=calculationInfo.timeMyr,
            rBoxKpc=calculationInfo.rBoxKpc
        )
        return self
    
    @abstractmethod
    def getData3d(self) \
        -> VelocityFilteringData3dReturnModel:
        pass
    
    @abstractmethod
    def getData2d(self, axis: str) \
        -> VelocityFilteringData2dReturnModel:
        pass
        