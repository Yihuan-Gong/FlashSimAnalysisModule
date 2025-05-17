import yt
import numpy as np
from typing import List, Tuple
from astropy import units as u

from .models import (
    YtTimeSeriesCalculationInfoModel,
    YtProfileCalculationInfoModel
)
from .models.interface import YtCalculationInfo
from ...models import (
    ProfileReturnModel,
    TimeSeriesReturnModel
)
from ......enum import Shape
from ......models import SimFileModel
from ......data_base import PandasHelper
from ......services import YtDsHelper, AstropyService
from ......utility import FieldAdder


class YtData1d:

    def __init__(self) -> None:
        FieldAdder.AddFields()
        

    def getTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: YtTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        result = []
        for timeMyr in calculationInfo.getTimeList():
            result.append(PandasHelper().getDataOrUpdateDb(
                simPath=simFile.simPath,
                dbFieldName=PandasHelper().getDbFieldName(calculationInfo.fieldName),
                funcToGetValue=self.__calculateValueFromYt(
                    simFile, calculationInfo.rKpc, timeMyr, calculationInfo
                ),
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
    
    
    def getProfileData(
        self,
        simFile: SimFileModel,
        calculationInfo: YtProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        if (calculationInfo.shape == Shape.Box):
            raise ValueError("Shape.Box is not supported")
        region = YtDsHelper().loadRegion(
            simFile, calculationInfo.shape, 
            calculationInfo.rEndKpc, calculationInfo.tMyr
        )
        prof = yt.Profile1D(
            data_source=region, 
            x_field=calculationInfo.radiusFieldName, 
            x_n=calculationInfo.getRList().__len__(), 
            x_min=u.Quantity(calculationInfo.rStartKpc, "kpc"), 
            x_max=u.Quantity(calculationInfo.rEndKpc, "kpc"), 
            x_log=False, 
            weight_field=calculationInfo.weightFieldName
        )
        prof.add_fields([calculationInfo.fieldName])
        
        y_val = prof[calculationInfo.fieldName]
        if str(y_val.units) == "dimensionless":
            y_array = y_val.value * u.dimensionless_unscaled
        else:
            y_array = y_val.to_astropy()
        
        return ProfileReturnModel(
            timeMyr=calculationInfo.tMyr,
            shape=calculationInfo.shape,
            rKpcList=prof.x.to_astropy().to("kpc").value,
            yValue=y_array
        )
        
    
    def __calculateValueFromYt(
        self,
        simFile: SimFileModel,
        rKpc: float,
        timeMyr: float,
        info: YtCalculationInfo
    ) -> u.Quantity:
        region = YtDsHelper().loadRegion(simFile, info.shape, rKpc, timeMyr)
        return region.quantities.weighted_average_quantity(
            info.fieldName, info.weightFieldName).to_astropy()
        
    