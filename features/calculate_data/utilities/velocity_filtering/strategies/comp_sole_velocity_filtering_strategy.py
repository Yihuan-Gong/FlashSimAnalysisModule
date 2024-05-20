from astropy import units as u

from .velocity_filtering_strategy import VelocityFilteringStrategy
from ..model import (
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from ..utilities import CompSoleFilter3d
from ......services import YtRawDataHelper
from ......utility import DataConverter, CellCoorCalculator


class CompSoleVelocityFilteringStrategy\
    (VelocityFilteringStrategy):
    
    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        result = self.getData3d()
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return VelocityFilteringData2dReturnModel(
            horizontalAxis=(axes[0], result.xAxis),
            verticalAxis=(axes[1], result.yAxis),
            compVx=DataConverter().data3dTo2dMiddle(result.compVx, axis),
            compVy=DataConverter().data3dTo2dMiddle(result.compVy, axis),
            compVz=DataConverter().data3dTo2dMiddle(result.compVz, axis),
            compVtotal=DataConverter().data3dTo2dMiddle(result.compVtotal, axis),
            soleVx=DataConverter().data3dTo2dMiddle(result.soleVx, axis),
            soleVy=DataConverter().data3dTo2dMiddle(result.soleVy, axis),
            soleVz=DataConverter().data3dTo2dMiddle(result.soleVz, axis),
            soleVtotal=DataConverter().data3dTo2dMiddle(result.soleVtotal, axis)
        )
    
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        (self._cube, self._cubeDims) = self._getVelocityRawDataCube()
        velx = self._cube[self._calculationInfo.velxFieldName].to_astropy()
        vely = self._cube[self._calculationInfo.velyFieldName].to_astropy()
        velz = self._cube[self._calculationInfo.velzFieldName].to_astropy()
        cellCoor: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=self._simFile, calculationInfo=self._calculationInfo
        )
        cellSize: u.Quantity = cellCoor[1] - cellCoor[0]
        
        compSoleFilter = CompSoleFilter3d(velx, vely, velz, cellSize)
        compSoleFilter.filter()
        result = VelocityFilteringData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            compVx=compSoleFilter.velxComp,
            compVy=compSoleFilter.velyComp,
            compVz=compSoleFilter.velzComp,
            compVtotal=self._calculateTotalVelocity(
                compSoleFilter.velxComp, 
                compSoleFilter.velyComp, 
                compSoleFilter.velzComp
            ),
            soleVx=compSoleFilter.velxSole,
            soleVy=compSoleFilter.velySole,
            soleVz=compSoleFilter.velzSole,
            soleVtotal=self._calculateTotalVelocity(
                compSoleFilter.velxSole,
                compSoleFilter.velySole,
                compSoleFilter.velzSole
            )
        )
        self._pickleService.saveIntoFile(result)
        return result
        
    
