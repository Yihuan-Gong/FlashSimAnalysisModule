from astropy import units as u
import numpy as np
import gc
from scipy.ndimage import uniform_filter

from .velocity_filtering_strategy import VelocityFilteringStrategy
from ..model import (
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
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
        cellSizeKpc = (cellCoor[1] - cellCoor[0]).to("kpc").value
        (self._cube, self._cubeDims) = self.__loadDataCube()
        avgDensity = self.__getAvgDensity(300, cellSizeKpc)

        result = VelocityFilteringData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            simonteVtotal=self.__calculateSimonteVelocity(avgDensity),
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
                self._calculationInfo.densityFieldName,
                self._calculationInfo.soundSpeedFieldName
            ]
        )
    
    
    # def __getAvgDensity(self, Lkpc: float, cellSizeKpc: float) -> u.Quantity:
    #     (densCube, densCubeDim) = YtRawDataHelper().loadRawData(
    #         simFile=self._simFile,
    #         timeMyr=self._calculationInfo.timeMyr,
    #         rBoxKpc=self._calculationInfo.rBoxKpc + Lkpc/2,
    #         fields=[self._calculationInfo.densityFieldName]
    #     )
        
    #     subBoxHalfLen = int(Lkpc / 2 / cellSizeKpc)
    #     minIndex = densCubeDim[0] // 2 - self._cubeDims[0]//2
    #     maxIndex = densCubeDim[0] // 2 + self._cubeDims[0]//2
    #     avgDensity = u.Quantity(np.zeros(self._cubeDims), "g/cm**3")
        
    #     for i in range(minIndex, maxIndex + 1):
    #         for j in range(minIndex, maxIndex + 1):
    #             for k in range(minIndex, maxIndex + 1):
    #                 avgDensity[i - minIndex, j - minIndex, k - minIndex] = \
    #                     densCube[self._calculationInfo.densityFieldName].to_astropy()[
    #                     i - subBoxHalfLen : i + subBoxHalfLen + 1,
    #                     j - subBoxHalfLen : j + subBoxHalfLen + 1,
    #                     k - subBoxHalfLen : k + subBoxHalfLen + 1
    #                 ].mean()
        
    #     return avgDensity
    
    def __getAvgDensity(self, Lkpc: float, cellSizeKpc: float) -> u.Quantity:
        (densCube, densCubeDim) = YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc + Lkpc/2,
            fields=[self._calculationInfo.densityFieldName]
        )
        
        subBoxHalfLen = int(Lkpc / 2 / cellSizeKpc)
        density = densCube[self._calculationInfo.densityFieldName].to_astropy()
        
        # Apply a uniform filter to compute the local mean over the subBoxHalfLen
        avgDensityCube = uniform_filter(density, size=(subBoxHalfLen * 2 + 1, subBoxHalfLen * 2 + 1, subBoxHalfLen * 2 + 1))
        
        # Extract the relevant sub-cube
        centerIndex = densCubeDim[0] // 2
        halfCubeDim = self._cubeDims[0] // 2
        startIndex = centerIndex - halfCubeDim
        endIndex = startIndex + self._cubeDims[0]
        avgDensity = avgDensityCube[startIndex:endIndex, startIndex:endIndex, startIndex:endIndex] * density.unit
        
        return avgDensity
    
    
    def __calculateSimonteVelocity(self, avgDensity: u.Quantity):
        density = self._cube[self._calculationInfo.densityFieldName].to_astropy()
        simonteVelocity: u.Quantity = (density - avgDensity)/avgDensity*\
            self._cube[self._calculationInfo.soundSpeedFieldName].to_astropy().to("cm/s")
        return np.abs(simonteVelocity)
        
        
    
        
        
        
        
    

    