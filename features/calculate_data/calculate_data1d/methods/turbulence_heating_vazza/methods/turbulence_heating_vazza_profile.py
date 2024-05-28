from typing import Iterable, List, Tuple
from astropy import units as u
import numpy as np

from ..models import (
    TurbulenceHeatingVazzaProfileCalculationInfoModel
)
from ....models import (
    ProfileReturnModel,
)
from ....utilities import Converter
from .....calculate_data3d import (
    Data3dAnalyzor,
    TurbulenceHeatingVazzaMode,
    TurbulenceHeatingVazzaCalculationInfoModel,
    TurbulenceHeatingVazzaData3dReturnModel
)
from .......models import SimFileModel
from .......enum import Shape


class TurbulenceHeatingVazzaProfile:
    
    def getProfile(
        self,
        powerMode: str,
        turbMode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        '''
        powerMode: "total" or "perVolume"
        
        Shape.Box is not supported
        '''
        if (calculationInfo.shape == Shape.Box):
            raise ValueError("Not supported")
        if (powerMode == "total"):
            return self.__heatingProfile(turbMode, simFile, calculationInfo)
        else:
            return self.__heatingPerVolumeProfile(turbMode, simFile, calculationInfo)
    
    
    def __heatingPerVolumeProfile(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        calcInfo3d = calculationInfo.toList()[-1]
        calcInfo3d.rBoxKpc = calculationInfo.rEndKpc
        data3d=Data3dAnalyzor().turbulenceHeatingVazza(
            mode=mode,
            simFile=simFile,
            calculationInfo=calcInfo3d
        )
        (rKpcList, heatingPerVolumeList) = Converter().data3dToProfile(
            data3d.heatingPerVolume, calculationInfo.getRList(), data3d.xAxis
        )
        return ProfileReturnModel(
            timeMyr=calculationInfo.tMyr,
            shape=calculationInfo.shape,
            rKpcList=rKpcList,
            yValue=heatingPerVolumeList
        )
    
    
    def __heatingProfile(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        heatingPerVol = self.__heatingPerVolumeProfile(
            mode, simFile, calculationInfo
        )
        return Converter().sphereIntegral(heatingPerVol)
        
    
