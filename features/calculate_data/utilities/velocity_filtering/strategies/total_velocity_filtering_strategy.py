from typing import Tuple, List
from astropy import units as u
import mirpyidl as idl
import numpy as np

from .velocity_filtering_strategy import VelocityFilteringStrategy
from ..model import (
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from ......services import YtRawDataHelper
from ......utility import DataConverter, CellCoorCalculator

class TotalVelocityFilteringStrategy(
    VelocityFilteringStrategy
):
    
    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        result = self.getData3d()
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return VelocityFilteringData2dReturnModel(
            horizontalAxis=(axes[0], result.xAxis),
            verticalAxis=(axes[1], result.yAxis),
            Vx=DataConverter().data3dTo2dMiddle(result.Vx, axis),
            Vy=DataConverter().data3dTo2dMiddle(result.Vy, axis),
            Vz=DataConverter().data3dTo2dMiddle(result.Vz, axis),
            Vtotal=DataConverter().data3dTo2dMiddle(result.Vtotal, axis)
        )
    
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        (cube, cubeDims) = self._getVelocityRawDataCube()
        cellCoor: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=self._simFile, calculationInfo=self._calculationInfo
        )
        # Vx=cube[self._calculationInfo.velxFieldName].to_astropy()
        # Vy=cube[self._calculationInfo.velyFieldName].to_astropy()
        # Vz=cube[self._calculationInfo.velzFieldName].to_astropy()
        # Vtotal = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        result = VelocityFilteringData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            Vx=cube[self._calculationInfo.velxFieldName].to_astropy(),
            Vy=cube[self._calculationInfo.velyFieldName].to_astropy(),
            Vz=cube[self._calculationInfo.velzFieldName].to_astropy(),
            Vtotal=None
        )
        self._pickleService.saveIntoFile(result)
        return result