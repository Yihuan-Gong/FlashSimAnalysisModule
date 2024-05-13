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
from ......models import SimFileModel
from ......data_base import PandasHelper, DbModel
from ......services import YtDsHelper, AstropyService
from ......utility import FieldAdder


class YtData1d:
    __xrayEmissivityField: Tuple[str, str] = ("gas","xray_emissivity_0.5_7.0_keV")
    __xrayLuminosityField: Tuple[str, str] = ("gas","xray_luminosity_0.5_7.0_keV")

    def __init__(self) -> None:
        FieldAdder.AddFields()
        

    def getTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: YtTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        result = []
        for timeMyr in calculationInfo.getTimeList():
            result.append(self.__getData(
                simFile=simFile,
                rKpc=calculationInfo.rKpc,
                timeMyr=timeMyr,
                info=calculationInfo
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
        result = []
        for rKpc in calculationInfo.getRList():
            result.append(self.__getData(
                simFile=simFile,
                rKpc=rKpc,
                timeMyr=calculationInfo.tMyr,
                info=calculationInfo
            ))
        return ProfileReturnModel(
            timeMyr=calculationInfo.tMyr,
            shape=calculationInfo.shape,
            rKpcList=calculationInfo.getRList(),
            yValue=AstropyService().quantityListToQuantity(result)
        )
        
    
    def __getData(
        self,
        simFile: SimFileModel,
        rKpc: float,
        timeMyr: float,
        info: YtCalculationInfo
    ) -> u.Quantity:
        value: u.Quantity
        
        # Field name for data base to give a file name to store calculated data
        dbFieldName = f"{info.fieldName[0]}_{info.fieldName[1]}"
        
        # Find the calculated result from data base
        data = PandasHelper().getDataFromCsv(
            simBasePath=simFile.simPath, 
            field=dbFieldName,  
            shape=info.shape, 
            rKpc=rKpc, 
            tMyr=timeMyr
        )
        if (data is not None):
            value = data["value"].to_list()[0] * u.Unit(data["valueUnit"].to_list()[0])
            return value
        
        # If the calculated result does not exist in data base,
        # we calculate one here
        value = self.__calculateValueFromYt(
            simFile=simFile,
            rKpc=rKpc,
            timeMyr=timeMyr,
            info=info
        )
        
        # Write the calculated result into data base
        PandasHelper().writeDataIntoCsv(
            simBasePath=simFile.simPath, 
            fieldName=dbFieldName,
            shape=info.shape,
            dbModelList=[DbModel(
                rKpc=rKpc, 
                tMyr=timeMyr, 
                value=float(value.value),
                valueUnit=value.unit
            )]
        )
        return value
    
    
    def __calculateValueFromYt(
        self,
        simFile: SimFileModel,
        rKpc: float,
        timeMyr: float,
        info: YtCalculationInfo
    ) -> u.Quantity:
        value: u.Quantity
        if (info.fieldName == self.__xrayEmissivityField or
            info.fieldName == self.__xrayLuminosityField):
            ds = YtDsHelper().loadDs(simFile, timeMyr, True)
            yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
            region = YtDsHelper().loadRegionFromDs(ds, info.shape, rKpc)
            value = region.quantities.total_quantity(info.fieldName).to_astropy()
        else:
            region = YtDsHelper().loadRegion(simFile, info.shape, rKpc, timeMyr)
            value = region.quantities.weighted_average_quantity(
                info.fieldName, info.weightFieldName).to_astropy()
        del region
        return value
    
        
    