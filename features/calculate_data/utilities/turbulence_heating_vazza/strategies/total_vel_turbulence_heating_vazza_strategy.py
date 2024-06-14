import numpy as np

from .turbulence_heating_vazza_strategy import TurbulenceHeatingVazzaStrategy
from ..models import (
    TurbulenceHeatingVazzaData3dReturnModel
)
from ...velocity_filtering import (
    VelocityFilteringMode,
)
from ......services import YtRawDataHelper


class TotalVelTurbulenceHeatingVazzaStrategy(
    TurbulenceHeatingVazzaStrategy
):
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        # Get bulk motion scall (driving scale)
        self._initVelocityFilter(VelocityFilteringMode.BulkTurb)
        velFilteringResult = self._velocityFilter.getData3d()
        
        # Get original velocity field
        totalVelocity = self.__getTotalVelFieldValue()
        
        heatingPerMass = self._calculateHeatingPerMass(
            velocity=totalVelocity,
            scale=velFilteringResult.scale
        )
        result = TurbulenceHeatingVazzaData3dReturnModel(
            xAxis=velFilteringResult.xAxis,
            yAxis=velFilteringResult.yAxis,
            zAxis=velFilteringResult.zAxis,
            heatingPerMass=heatingPerMass,
            heatingPerVolume=self._calculateHeatingPerVolume(heatingPerMass),
            scale=velFilteringResult.scale
        )
        self._pickleService.saveIntoFile(result)
        return result
    
    
    def __getTotalVelFieldValue(self):
        (cube, cubeDims) = YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc,
            fields=[
                self._calculationInfo.velxFieldName,
                self._calculationInfo.velyFieldName,
                self._calculationInfo.velzFieldName
            ]
        )
        return np.sqrt(
            cube[self._calculationInfo.velxFieldName]**2 + \
            cube[self._calculationInfo.velyFieldName]**2 + \
            cube[self._calculationInfo.velzFieldName]**2
        ).to_astropy()