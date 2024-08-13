from astropy import units as u
import numpy as np
import gc
from scipy.ndimage import uniform_filter
from scipy.interpolate import interp1d

from ..models import (
    DensityFilteringCalculationInfoModel,
    DensityFilteringData3dReturnModel,
    DensityFilteringData2dReturnModel
)
from ....calculate_data1d.methods.yt import (
    YtData1d,
    YtProfileCalculationInfoModel
)
from ......models import SimFileModel
from ......services import YtRawDataHelper, PickleService
from ......utility import DataConverter, CellCoorCalculator
from ......enum import Shape


class DensityFilteringMethod:
    _simFile: SimFileModel
    _calculationInfo: DensityFilteringCalculationInfoModel
    _pickleService: PickleService
    
    
    def setInputs(self, simFile: SimFileModel, calculationInfo: DensityFilteringCalculationInfoModel):
        self._simFile = simFile
        self._calculationInfo = calculationInfo
        self._pickleService = PickleService(
            simPath=simFile.simPath,
            prefix=self.__class__.__name__,
            timeMyr=calculationInfo.timeMyr,
            rBoxKpc=calculationInfo.rBoxKpc,
        )
        
    
    def getData2d(self, axis: str) -> DensityFilteringData2dReturnModel:
        result = self.getData3d()
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return DensityFilteringData2dReturnModel(
            rho=DataConverter().data3dTo2dMiddle(result.rho, axis),
            deltaRho=DataConverter().data3dTo2dMiddle(result.deltaRho, axis),
            horizontalAxis=(axes[0], result.xAxis),
            verticalAxis=(axes[1], result.yAxis)
        )
    
    
    def getData3d(self) -> DensityFilteringData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        gc.disable()
        
        cellCoor: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=self._simFile, calculationInfo=self._calculationInfo
        )
        cellSizeKpc = (cellCoor[1] - cellCoor[0]).to("kpc").value
        (self._cube, self._cubeDims) = self.__loadDataCube()
        
        density = self._cube[self._calculationInfo.densityFieldName].to_astropy()
        if (self._calculationInfo.densityFilteringMode == "box"):
            avgDensity = self.__getBoxAvgDensity(300, cellSizeKpc)
        elif (self._calculationInfo.densityFilteringMode == "radial"):
            avgDensity = self.__getRadialAvgDensity(cellSizeKpc)
        else:
            raise ValueError("self.__densAvgMode invalid")

        result = DensityFilteringData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            rho=density,
            deltaRho=density - avgDensity,
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
            ]
        )
    
    
    def __getBoxAvgDensity(self, Lkpc: float, cellSizeKpc: float) -> u.Quantity:
        (densCube, densCubeDim) = YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc + Lkpc/2,
            fields=[self._calculationInfo.densityFieldName]
        )
        
        subBoxHalfLen = int(Lkpc / 2 / cellSizeKpc)
        density = densCube[self._calculationInfo.densityFieldName].to_astropy()
        
        # Apply a uniform filter to compute the local mean over the subBoxHalfLen
        avgDensityCube = uniform_filter(
            density, size=(subBoxHalfLen * 2 + 1, subBoxHalfLen * 2 + 1, subBoxHalfLen * 2 + 1))
        
        # Extract the relevant sub-cube
        centerIndex = densCubeDim[0] // 2
        halfCubeDim = self._cubeDims[0] // 2
        startIndex = centerIndex - halfCubeDim
        endIndex = startIndex + self._cubeDims[0]
        avgDensity = avgDensityCube[startIndex:endIndex, startIndex:endIndex, startIndex:endIndex] * density.unit
        
        return avgDensity
    
    
    def __getRadialAvgDensity(self, cellSizeKpc: float) -> u.Quantity:
        densProfile = YtData1d().getProfileData(
            self._simFile, 
            YtProfileCalculationInfoModel(
                tMyr=self._calculationInfo.timeMyr,
                rStartKpc=0,
                rEndKpc=self._calculationInfo.rBoxKpc*np.sqrt(3),
                rStepKpc=cellSizeKpc,
                shape=Shape.Sphere,
                fieldName=self._calculationInfo.densityFieldName
            )
        )
        return self.__profileTo3d(
            self._cubeDims[0],
            densProfile.yValue,
            u.Quantity(densProfile.rKpcList, "kpc"),
            u.Quantity(cellSizeKpc, "kpc")
        )
    
    
    def __profileTo3d(self, dim: int, radialProfile: u.Quantity, radius: u.Quantity, cellSize: u.Quantity) -> u.Quantity:
        # 創建插值函數
        interp_func = interp1d(radius, radialProfile, kind='linear', fill_value="extrapolate")

        # 創建三維網格
        x = np.linspace(-dim//2, dim//2, dim) * cellSize
        y = np.linspace(-dim//2, dim//2, dim) * cellSize
        z = np.linspace(-dim//2, dim//2, dim) * cellSize
        xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')

        # 計算距離
        distances = np.sqrt(xx**2 + yy**2 + zz**2)

        # 插值得到密度值
        array3d = interp_func(distances)

        # 將結果轉換為astropy.unit.Quantity
        array3d = array3d * radialProfile.unit
        return array3d
    
