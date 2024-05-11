from .turbulence_heating_vazza_strategy import TurbulenceHeatingVazzaStrategy
from ..models import (
    TurbulenceHeatingVazzaData2dReturnModel,
    TurbulenceHeatingVazzaData3dReturnModel
)
from ...velocity_filtering import (
    VelocityFilteringMode,
)
from ......utility import DataConverter

class TurbVelTurbulenceHeatingVazzaStrategy(
    TurbulenceHeatingVazzaStrategy
):
    velocityFilteringMode = VelocityFilteringMode.BulkTurb
    
    def getData2d(self, axis: str) -> TurbulenceHeatingVazzaData2dReturnModel:
        self._initVelocityFilter(self.velocityFilteringMode)
        result3d = self.getData3d()
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return TurbulenceHeatingVazzaData2dReturnModel(
            heatingPerMass=DataConverter().data3dTo2dMiddle(result3d.heatingPerMass, axis),
            heatingPerVolume=DataConverter().data3dTo2dMiddle(result3d.heatingPerVolume, axis),
            scale=DataConverter().data3dTo2dMiddle(result3d.scale, axis),
            horizontalAxis=(axes[0], result3d.xAxis),
            verticalAxis=(axes[1], result3d.yAxis)
        )
    
    
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        self._initVelocityFilter(self.velocityFilteringMode)
        velFilteringResult = self._velocityFilter.getData3d()
        heatingPerMass = self._calculateHeatingPerMass(
            velocity=velFilteringResult.turbVtotal,
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
        
        
    
        
    
    