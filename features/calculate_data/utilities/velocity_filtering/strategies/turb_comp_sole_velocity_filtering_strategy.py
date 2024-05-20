from astropy import units as u

from .velocity_filtering_strategy import VelocityFilteringStrategy
from .bulk_turb_velocity_filtering_strategy import BulkTurbVelocityFilteringStrategy
from ..model import (
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from ..utilities import CompSoleFilter3d
from ......utility import DataConverter


class TurbCompSoleVelocityFilteringStrategy(
    VelocityFilteringStrategy
):
    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        result = self.getData3d()
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return VelocityFilteringData2dReturnModel(
            horizontalAxis=(axes[0], result.xAxis),
            verticalAxis=(axes[1], result.yAxis),
            turbCompVx=DataConverter().data3dTo2dMiddle(result.turbCompVx, axis),
            turbCompVy=DataConverter().data3dTo2dMiddle(result.turbCompVy, axis),
            turbCompVz=DataConverter().data3dTo2dMiddle(result.turbCompVz, axis),
            turbCompVtotal=DataConverter().data3dTo2dMiddle(result.turbCompVtotal, axis),
            turbSoleVx=DataConverter().data3dTo2dMiddle(result.turbSoleVx, axis),
            turbSoleVy=DataConverter().data3dTo2dMiddle(result.turbSoleVy, axis),
            turbSoleVz=DataConverter().data3dTo2dMiddle(result.turbSoleVz, axis),
            turbSoleVtotal=DataConverter().data3dTo2dMiddle(result.turbSoleVtotal, axis)
        )
    
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result

        turbResult = BulkTurbVelocityFilteringStrategy().setInputs(
            simFile=self._simFile,
            calculationInfo=self._calculationInfo
        ).getData3d()
        
        cellSize: u.Quantity = turbResult.xAxis[1] - turbResult.xAxis[0]
        compSoleFilter = CompSoleFilter3d(
            turbResult.turbVx, turbResult.turbVy, turbResult.turbVz, cellSize)
        compSoleFilter.filter()
        
        result = VelocityFilteringData3dReturnModel(
            xAxis=turbResult.xAxis,
            yAxis=turbResult.yAxis,
            zAxis=turbResult.zAxis,
            turbCompVx=compSoleFilter.velxComp,
            turbCompVy=compSoleFilter.velyComp,
            turbCompVz=compSoleFilter.velzComp,
            turbCompVtotal=self._calculateTotalVelocity(
                compSoleFilter.velxComp, 
                compSoleFilter.velyComp, 
                compSoleFilter.velzComp
            ),
            turbSoleVx=compSoleFilter.velxSole,
            turbSoleVy=compSoleFilter.velySole,
            turbSoleVz=compSoleFilter.velzSole,
            turbSoleVtotal=self._calculateTotalVelocity(
                compSoleFilter.velxSole,
                compSoleFilter.velySole,
                compSoleFilter.velzSole
            )
        )
        self._pickleService.saveIntoFile(result)
        return result
        