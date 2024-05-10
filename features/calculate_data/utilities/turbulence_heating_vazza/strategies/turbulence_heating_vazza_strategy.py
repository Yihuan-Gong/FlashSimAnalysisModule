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
from ......services import YtRawDataHelper


class TurbulenceHeatingVazzaStrategy(ABC):
    _simFile: SimFileModel
    _calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    _velocityFilter: VelocityFiltering
    
    def setInputs(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    ):
        self._calculationInfo = calculationInfo
        self._simFile = simFile
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
    
    
    def _calculateDisspationRate(
        self, 
        velocity: u.Quantity, 
        scale: u.Quantity,
    ) -> u.Quantity:
        dissipationRate = (0.5*velocity**3/scale).unit.cgs
        density = YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc,
            fields=[self._calculationInfo.densityFieldName]
        )[0][self._calculationInfo.densityFieldName].to_astropy()
        return density*dissipationRate

