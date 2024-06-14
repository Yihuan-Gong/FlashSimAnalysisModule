import yt
import numpy as np
from typing import List, Tuple
from astropy import units as u

from .models import (
    XrayProfileCalculationInfoModel,
    XrayTimeSeriesCalculationInfoModel
)
from .models.interface import XrayCalculationInfo
from ...utilities import Converter
from ...models import (
    ProfileReturnModel,
    TimeSeriesReturnModel
)
from ......enum import Shape
from ......models import SimFileModel
from ......data_base import PandasHelper
from ......services import YtDsHelper, AstropyService
from ......utility import FieldAdder


class XrayData1d:

    def __init__(self) -> None:
        FieldAdder.AddFields()
        

    def getXrayEmissivityProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: XrayProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        '''
        Please use smaller rStepKpc to get smoother curve. The smaller rStepKpc
        is, the more accurate the result is. Using smaller rStepKpc will not result in longer
        runtime, since the bottom of getXrayEmissivityProfile() is yt.Profile1D
        '''
        if (calculationInfo.shape == Shape.Box):
            raise ValueError("Shape.Box is not supported")
        region = self.__regionLoader(
            simFile, calculationInfo.tMyr, calculationInfo.rEndKpc, 
            calculationInfo.shape, calculationInfo
        )
        prof = yt.Profile1D(
            data_source=region, 
            x_field=FieldAdder.getRadiusFieldName(), 
            x_n=calculationInfo.getRList().__len__()-1, 
            x_min=u.Quantity(calculationInfo.rStartKpc, "kpc"), 
            x_max=u.Quantity(calculationInfo.rEndKpc-calculationInfo.rStepKpc, "kpc"), 
            x_log=False, 
            weight_field=calculationInfo.weightFieldName
        )
        prof.add_fields([calculationInfo.getXrayEmissivityFieldName()])
        return ProfileReturnModel(
            timeMyr=calculationInfo.tMyr,
            shape=calculationInfo.shape,
            rKpcList=prof.x.to_astropy().to("kpc").value,
            yValue=prof[calculationInfo.getXrayEmissivityFieldName()].to_astropy()
        )
    
    
    def getXrayEmissivityTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: XrayTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        return self.__getXrayTimeSeries(
            mode="emissivity",
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def getXrayLuminosityProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: XrayProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        '''
        This method automatically do volume intergral from the result of
        getXrayEmissivityProfile(). So please use smaller rStepKpc. The smaller rStepKpc
        is, the more accurate the result is. Using smaller rStepKpc will not result in longer
        runtime, since the bottom of getXrayEmissivityProfile() is yt.Profile1D
        '''
        if (calculationInfo.shape == Shape.Box):
            raise ValueError("Shape.Box is not supported")
        
        xrayEmissData = self.getXrayEmissivityProfile(simFile, calculationInfo)
        return Converter().sphereIntegral(xrayEmissData)
    
    
    def getXrayLuminosityTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: XrayTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        return self.__getXrayTimeSeries(
            mode="luminosity",
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def __getXrayTimeSeries(
        self,
        mode: str,
        simFile: SimFileModel,
        calculationInfo: XrayTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        fieldName: Tuple[str, str]
        if (mode == "emissivity"):
            fieldName = calculationInfo.getXrayEmissivityFieldName()
        else:
            fieldName = calculationInfo.getXrayLuminosityFieldName()
        
        result = []
        for timeMyr in calculationInfo.getTimeList():
            result.append(PandasHelper().getDataOrUpdateDb(
                simPath=simFile.simPath,
                dbFieldName=PandasHelper().getDbFieldName(fieldName),
                funcToGetValue=lambda: self.__calculateXrayData(
                    mode, timeMyr, simFile, calculationInfo),
                rKpc=calculationInfo.rKpc,
                timeMyr=timeMyr,
                shape=calculationInfo.shape
            ))
        return TimeSeriesReturnModel(
            rKpc=calculationInfo.rKpc,
            shape=calculationInfo.shape,
            timeMyrList=calculationInfo.getTimeList(),
            yValue=AstropyService().quantityListToQuantity(result)
        )
    
    
    def __calculateXrayData(
        self,
        mode: str,
        timeMyr: float,
        simFile: SimFileModel,
        info: XrayTimeSeriesCalculationInfoModel
    ) -> u.Quantity:
        region = self.__regionLoader(simFile, timeMyr, info.rKpc, info.shape, info)
        if (mode == "emissivity"):
            return region.quantities.weighted_average_quantity(
                info.getXrayEmissivityFieldName(), info.weightFieldName).to_astropy()
        else:
            return region.quantities.total_quantity(
                info.getXrayLuminosityFieldName()).to_astropy()
        
    
    def __regionLoader(
        self,
        simFile: SimFileModel,
        timeMyr: float,
        rKpc: float,
        shape: Shape,
        info: XrayCalculationInfo
    ):
        ds = YtDsHelper().loadDs(simFile, timeMyr, True)
        info.addXrayFields(ds)
        return YtDsHelper().loadRegionFromDs(ds, shape, rKpc)
    
    
    