from abc import ABC, abstractmethod
from astropy import units as u

from ..models import (
    TurbulenceHeatingVazzaData2dReturnModel,
    TurbulenceHeatingVazzaData3dReturnModel,
    TurbulenceHeatingVazzaCalculationInfoModel
)
from ...velocity_filtering import (
    VelocityFiltering,
    VelocityFilteringMode
) 
from ......models import SimFileModel
from ......services import YtRawDataHelper, PickleService


class TurbulenceHeatingVazzaStrategy(ABC):
    _simFile: SimFileModel
    _calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    _velocityFilter: VelocityFiltering
    _pickleService: PickleService
    
    def setInputs(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    ):
        self._calculationInfo = calculationInfo
        self._simFile = simFile
        self._pickleService = PickleService(
            simPath=simFile.simPath,
            prefix=self.__class__.__name__,
            timeMyr=calculationInfo.timeMyr,
            rBoxKpc=calculationInfo.rBoxKpc
        )
        return self
    
    
    @abstractmethod
    def getData2d(self, axis: str) -> TurbulenceHeatingVazzaData2dReturnModel:
        pass
    
    
    @abstractmethod
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        pass
    
    
    def _initVelocityFilter(self, mode: VelocityFilteringMode):
        self._velocityFilter = VelocityFiltering().setInputs(
            mode=mode,
            simFile=self._simFile,
            calculationInfo=self._calculationInfo
        )
    
    
    def _calculateHeatingPerVolume(
        self, 
        heatingPerMass: u.Quantity,
    ) -> u.Quantity:
        density: u.Quantity = YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc,
            fields=[self._calculationInfo.densityFieldName]
        )[0][self._calculationInfo.densityFieldName].to_astropy()
        result = density*heatingPerMass
        return result.to("erg/(s*cm**3)")
    
    
    def _calculateHeatingPerMass(
        self, 
        velocity: u.Quantity, 
        scale: u.Quantity,
    ) -> u.Quantity:
        result = 0.5*velocity**3/scale
        return result.to("erg/(s*g)")

