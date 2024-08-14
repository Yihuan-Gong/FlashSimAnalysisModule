from typing import Tuple
from astropy import units as u
import numpy as np
import gc

from .velocity_filtering_strategy import VelocityFilteringStrategy
from ..model import (
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from ...yt_field import *
from ......services import YtRawDataHelper
from ......utility import DataConverter, CellCoorCalculator

class SimonteVelocityFilteringStrategy(
    VelocityFilteringStrategy
):

    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        result = self.getData3d()
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return VelocityFilteringData2dReturnModel(
            simonteVtotal=DataConverter().data3dTo2dMiddle(result.simonteVtotal, axis),
            horizontalAxis=(axes[0], result.xAxis),
            verticalAxis=(axes[1], result.yAxis)
        )
        
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        gc.disable()
        
        cellCoor: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=self._simFile, calculationInfo=self._calculationInfo
        )
        
        result = VelocityFilteringData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            simonteVtotal=self.__calculateSimonteVelocity(),
        )
        self._pickleService.saveIntoFile(result)
        
        gc.enable()
        
        return result
        
        
    def __loadDataCube(self):
        return YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc,
            fields=[
                self._calculationInfo.soundSpeedFieldName
            ]
        )
    
    
    def __calculateSimonteVelocity(self):
        rho = self.__getYtFieldResult(self._calculationInfo.densityFieldName)
        cs = self.__getYtFieldResult(self._calculationInfo.soundSpeedFieldName)
        
        #deltaRho/rhoAvg*soundSpeed
        simonteVelocity: u.Quantity = rho.radialAvgFilteredFieldValue/rho.radialAvgFieldValue*cs.radialAvgFieldValue
        return simonteVelocity
    
    
    def __getYtFieldResult(self, fieldName: Tuple[str, str]):
        return YtField().getRadialAvgFilteredValue(
            self._simFile,
            calculationInfo=YtFieldCalculationInfoModel(
                timeMyr=self._calculationInfo.timeMyr,
                rBoxKpc=self._calculationInfo.rBoxKpc,
                fieldName=fieldName
            )
        )
        