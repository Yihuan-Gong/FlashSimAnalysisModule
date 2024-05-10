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
            heating=DataConverter().data3dTo2dMiddle(result3d.heating, axis),
            scale=DataConverter().data3dTo2dMiddle(result3d.scale, axis),
            horizontalAxis=(axes[0], result3d.xAxis),
            verticalAxis=(axes[1], result3d.yAxis)
        )
    
    
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        self._initVelocityFilter(self.velocityFilteringMode)
        velFilteringResult = self._velocityFilter.getData3d()
        return TurbulenceHeatingVazzaData3dReturnModel(
            xAxis=velFilteringResult.xAxis,
            yAxis=velFilteringResult.yAxis,
            zAxis=velFilteringResult.zAxis,
            heating=self._calculateDisspationRate(
                velocity=velFilteringResult.turbVtotal,
                scale=velFilteringResult.scale
            ),
            scale=velFilteringResult.scale
        )
        
        
    
        
    
    