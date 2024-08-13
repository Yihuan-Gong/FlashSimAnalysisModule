from astropy import units as u
import numpy as np
import gc
from scipy.ndimage import uniform_filter
from scipy.interpolate import interp1d

from .models import YtFieldCalculationInfoModel, YtFieldData3dReturnModel
from ...calculate_data1d.methods.yt import (
    YtData1d,
    YtProfileCalculationInfoModel
)
from .....enum import Shape
from .....models import SimFileModel
from .....services import YtRawDataHelper
from .....utility import CellCoorCalculator

class YtField:
    
    def getFieldValue(self, simFile: SimFileModel, calculationInfo: YtFieldCalculationInfoModel):
        cellCoor: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=simFile, calculationInfo=calculationInfo
        )
        (cube, cubeDims) = YtRawDataHelper().loadRawData(
            simFile=simFile,
            timeMyr=calculationInfo.timeMyr,
            rBoxKpc=calculationInfo.rBoxKpc,
            fields=[
                calculationInfo.fieldName,
            ]
        )
        return YtFieldData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            fieldValue=cube[calculationInfo.fieldName].to_astropy()
        )
        
    
    def getRadialAvgFilteredValue(self, simFile: SimFileModel, calculationInfo: YtFieldCalculationInfoModel):
        result = self.getFieldValue(simFile, calculationInfo)
        result.radialAvgFieldValue = self.__getRadialAvgValue(
            simFile, 
            calculationInfo, 
            result.xAxis.__len__(), 
            (result.xAxis[1]-result.xAxis[0]).to("kpc").value
        )
        result.radialAvgFilteredFieldValue = result.fieldValue - result.radialAvgFieldValue
        return result
        
        
        
    
    
    def __getRadialAvgValue(self, simFile: SimFileModel, calculationInfo: YtFieldCalculationInfoModel, cubeDim: int, cellSizeKpc: float) -> u.Quantity:
        densProfile = YtData1d().getProfileData(
            simFile, 
            YtProfileCalculationInfoModel(
                tMyr=calculationInfo.timeMyr,
                rStartKpc=0,
                rEndKpc=calculationInfo.rBoxKpc*np.sqrt(3),
                rStepKpc=cellSizeKpc,
                shape=Shape.Sphere,
                fieldName=calculationInfo.fieldName
            )
        )
        return self.__profileTo3d(
            cubeDim,
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
    
