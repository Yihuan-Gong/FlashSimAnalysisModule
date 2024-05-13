from typing import List, Tuple
from astropy import units as u

from .models import (
    TurbulenceHeatingProfileCalculationInfoModel,
    TurbulenceHeatingTimeSeriesCalculationInfoModel,
    TurbulenceHeatingProfileReturnModel,
    TurbulenceHeatingTimeSeriesReturnModel
)
from ......models import SimFileModel
from ......data_base import DbModel, TurbDbModel, TurbPandasHelper
from ......enum import Shape
from ......services import YtDsHelper
from ......utility.turbulence_analyzor import TurbulenceAnalyzor


class TurbulenceHeatingData1d:
    __turbHeatingUnit: u.Quantity = 1*u.Unit("erg/s")

    
    def getTimeSeriesData(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingTimeSeriesCalculationInfoModel
    ) -> TurbulenceHeatingTimeSeriesReturnModel:
        if (calculationInfo.shape != Shape.Box):
            raise ValueError("Turbulence heating only support box shape!")
        turbHeatingUpper: List[float] = []
        turbHeatingLower: List[float] = []
        for timeMyr in calculationInfo.getTimeList():
            data = self.__getHeatingRate(
                simFile=simFile,
                rKpc=calculationInfo.rKpc,
                timeMyr=timeMyr,
                shape=calculationInfo.shape,
                rhoIndex=calculationInfo.rhoIndex
            )
            turbHeatingLower.append(data[0])
            turbHeatingUpper.append(data[1])
        
        return TurbulenceHeatingTimeSeriesReturnModel(
            rKpc=calculationInfo.rKpc,
            shape=calculationInfo.shape,
            rhoIndex=calculationInfo.rhoIndex,
            timeMyrList=calculationInfo.getTimeList(),
            upperLimit=turbHeatingUpper*self.__turbHeatingUnit,
            lowerLimit=turbHeatingLower*self.__turbHeatingUnit
        )
        
    
    def getProfileData(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingProfileCalculationInfoModel
    ) -> TurbulenceHeatingProfileReturnModel:
        if (calculationInfo.shape != Shape.Box):
            raise ValueError("Turbulence heating only support box shape!")
        turbHeatingUpper: List[float] = []
        turbHeatingLower: List[float] = []
        for rKpc in calculationInfo.getRList():
            data = self.__getHeatingRate(
                simFile=simFile,
                rKpc=rKpc,
                timeMyr=calculationInfo.tMyr,
                shape=calculationInfo.shape,
                rhoIndex=calculationInfo.rhoIndex
            )
            turbHeatingLower.append(data[0])
            turbHeatingUpper.append(data[1])
        
        return TurbulenceHeatingProfileReturnModel(
            timeMyr=calculationInfo.tMyr,
            shape=calculationInfo.shape,
            rhoIndex=calculationInfo.rhoIndex,
            rKpcList=calculationInfo.getRList(),
            upperLimit=turbHeatingUpper*self.__turbHeatingUnit,
            lowerLimit=turbHeatingLower*self.__turbHeatingUnit
        )
    
    
    def __getHeatingRate(
        self, 
        simFile: SimFileModel,
        rKpc: float,
        timeMyr: float,
        shape: Shape,
        rhoIndex: float,
    ) -> Tuple[float, float]:
        turbData = TurbPandasHelper().getTurbDataFromCsv(
            simBasePath=simFile.simPath,
            shape=shape,
            rKpc=rKpc,
            tMyr=timeMyr,
            rhoIndex=rhoIndex
        )
        if (turbData is not None):
            return (turbData.lowerLimit, turbData.upperLimit)

        ds = YtDsHelper().loadDs(simFile, timeMyr)
        turbDataTemp = TurbulenceAnalyzor()\
            .setDensityWeightingIndex(rhoIndex) \
            .setDataSeries(ds) \
            .setBoxSize(rKpc) \
            .calculatePowerSpectrum() \
            .getDissipationRate()
        turbData = TurbDbModel(
            rhoIndex=rhoIndex,
            upperLimit=turbDataTemp["turb_heating_rate_upper_limit"],
            lowerLimit=turbDataTemp["turb_heating_rate_lower_limit"]
        )
        TurbPandasHelper().writeDataIntoCsv(
            simBasePath=simFile.simPath, 
            fieldName="TurbulenceHeating", 
            shape=shape,
            dbModelList=[DbModel(
                rKpc=rKpc, 
                tMyr=timeMyr, 
                value=turbData,
                valueUnit=None
            )]
        )
        return (turbData.lowerLimit, turbData.upperLimit)
