from typing import List
from astropy import units as u

from .models import TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
from ...models import (
    ProfileReturnModel,
    TimeSeriesReturnModel
)
from ....calculate_data3d import (
    Data3dAnalyzor,
    TurbulenceHeatingVazzaMode,
    TurbulenceHeatingVazzaCalculationInfoModel,
)
from ......models import SimFileModel
from ......enum import Shape
from ......data_base import PandasHelper, DbModel
from ......services import AstropyService



class TurbulenceHeatingVazzaData1d:
    __dbFieldName: str = "TurbulenceHeatingVazza"

    
    def getTimeSeries(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
    ):
        if (calculationInfo.shape == Shape.Sphere):
            raise ValueError("So far Shape.Shpere is not implemented. \
                Hope that I will implement this some day.")
        
        result: List[u.Quantity] = []
        for calcInfoData3d in calculationInfo.toList():
            result.append(self.__calcHeatingRate(
                shape=calculationInfo.shape,
                mode=mode,
                simFile=simFile,
                calcInfo3d=calcInfoData3d
            ))
        
        return TimeSeriesReturnModel(
            rKpc=calculationInfo.rKpc,
            shape=calculationInfo.shape,
            timeMyrList=calculationInfo.getTimeList(),
            yValue=AstropyService().quantityListToQuantity(result)
        )
        
    
    def __calcHeatingRate(
        self,
        shape: Shape,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calcInfo3d: TurbulenceHeatingVazzaCalculationInfoModel
    ) -> u.Quantity:
        '''
        Currently can only be used for Shape.Box
        '''
        df = PandasHelper().getDataFromCsv(
            simBasePath=simFile.simPath,
            field=self.__dbFieldName,
            shape=shape,
            rKpc=calcInfo3d.rBoxKpc,
            tMyr=calcInfo3d.timeMyr
        )
        if (df is not None):
            return df["value"].to_list()[0]*\
                u.Unit(df["valueUnit"].to_list()[0])
        
        data3d = Data3dAnalyzor().turbulenceHeatingVazza(
            mode=mode,
            simFile=simFile,
            calculationInfo=calcInfo3d
        )
        heatingRate: u.Quantity = (data3d.heatingPerVolume.mean()*\
            (2.*calcInfo3d.rBoxKpc*u.Unit("kpc"))**3).to("erg/s")
        
        PandasHelper().writeDataIntoCsv(
            simBasePath=simFile.simPath,
            fieldName=self.__dbFieldName,
            shape=shape,
            dbModelList=[DbModel(
                rKpc=calcInfo3d.rBoxKpc,
                tMyr=calcInfo3d.timeMyr,
                value=float(heatingRate.value),
                valueUnit=heatingRate.unit.to_string()
            )]
        )
        return heatingRate
            
        