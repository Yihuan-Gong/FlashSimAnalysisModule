from typing import List, Tuple
from astropy import units as u
import numpy as np

from .models import (
    TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel,
    TurbulenceHeatingVazzaProfileCalculationInfoModel
)
from ...models import (
    ProfileReturnModel,
    TimeSeriesReturnModel
)
from ....calculate_data3d import (
    Data3dAnalyzor,
    TurbulenceHeatingVazzaMode,
    TurbulenceHeatingVazzaCalculationInfoModel,
    TurbulenceHeatingVazzaData3dReturnModel
)
from ......models import SimFileModel
from ......enum import Shape
from ......data_base import PandasHelper, DbModel
from ......services import AstropyService


class TurbulenceHeatingVazzaData1d:
    
    def getTimeSeries(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
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
    
    # To do: profile不能用DB(?)
    def getProfile(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        result: List[u.Quantity] = []
        for calcInfoData3d in calculationInfo.toList():
            result.append(self.__calcHeatingRate(
                shape=calculationInfo.shape,
                mode=mode,
                simFile=simFile,
                calcInfo3d=calcInfoData3d,
                rBoxRequestKpc=calculationInfo.rEndKpc
            ))
        
        return ProfileReturnModel(
            timeMyr=calculationInfo.tMyr,
            shape=calculationInfo.shape,
            rKpcList=calculationInfo.getRList(),
            yValue=AstropyService().quantityListToQuantity(result)
        )
    
    
    def __calcHeatingRate(
        self,
        shape: Shape,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calcInfo3d: TurbulenceHeatingVazzaCalculationInfoModel,
        rBoxRequestKpc: float = None
    ) -> u.Quantity:
        '''
        rBoxRequestKpc: This function will use Data3d automatically to calculate
        heating rate. Using this parameter you can manually assign the box size
        used for Data3d calculation. However, the final result of the heating rate
        will not depend on this parameter. This parameter can only be used for enhancing
        performance if you want to calculate the heating rate within the region smaller
        than you have calculated before. Here's examples
        
        Ex1: 
        calcInfo3d.rBoxKpc=100kpc;  
        rBoxRequestKpc=200kpc
        => Calculate total heating rate within 100kpc
        
        Ex2:
        calcInfo3d.rBoxKpc=200kpc;  
        rBoxRequestKpc=100kpc
        => Invalid!
        '''
        if (rBoxRequestKpc is None):
            rBoxRequestKpc = calcInfo3d.rBoxKpc
        if (rBoxRequestKpc < calcInfo3d.rBoxKpc):
            raise ValueError("rBoxRequestKpc should be at least 2 cells per side larger than calcInfo3d.rBoxKpc")
        
        dbFieldName: str = "TurbulenceHeatingVazza_" + f"{mode}".split(".")[-1]
        df = PandasHelper().getDataFromCsv(
            simBasePath=simFile.simPath,
            field=dbFieldName,
            shape=shape,
            rKpc=calcInfo3d.rBoxKpc,
            tMyr=calcInfo3d.timeMyr
        )
        if (df is not None):
            return df["value"].to_list()[0]*\
                u.Unit(df["valueUnit"].to_list()[0])
        
        rKpcForHeatingRate = calcInfo3d.rBoxKpc
        calcInfo3d.rBoxKpc = rBoxRequestKpc
        data3d = Data3dAnalyzor().turbulenceHeatingVazza(
            mode=mode,
            simFile=simFile,
            calculationInfo=calcInfo3d
        )
        heatingRate: u.Quantity = self.__geHeatingRateWithinRegion(
            shape, rKpcForHeatingRate, data3d
        )
        
        PandasHelper().writeDataIntoCsv(
            simBasePath=simFile.simPath,
            fieldName=dbFieldName,
            shape=shape,
            dbModelList=[DbModel(
                rKpc=rKpcForHeatingRate,
                tMyr=calcInfo3d.timeMyr,
                value=float(heatingRate.value),
                valueUnit=heatingRate.unit.to_string()
            )]
        )
        return heatingRate
    
    
    def __geHeatingRateWithinRegion(
        self,
        shape: Shape,
        rKpc: float,
        data3d: TurbulenceHeatingVazzaData3dReturnModel
    ) -> u.Quantity:
        cellSizeKpc = (data3d.xAxis[1]-data3d.xAxis[0]).to("kpc").value
        n = data3d.xAxis.__len__()
        diff = np.abs(data3d.xAxis.to("kpc").value - cellSizeKpc/2.)
        mid = np.argmin(diff)
        n_inner_region = int(np.floor(rKpc/cellSizeKpc)-1)
        n_outer_region = int(np.floor(rKpc/cellSizeKpc))
        if (mid - n_outer_region < 0 or mid + n_outer_region >= n):
            raise ValueError("Region given should be smaller than the size of data3d")
        
        if (shape == Shape.Box):
            return self.__getHeatingRateWithinBoxRegion(
                rKpc, cellSizeKpc, mid, n_inner_region, n_outer_region, data3d)
        else:
            return self.__getHeatingRateWithinSphereRegion(
                rKpc, cellSizeKpc, mid, n_inner_region, n_outer_region, data3d)
    
    
    def __getHeatingRateWithinBoxRegion(
        self,
        rBoxKpc: float,
        cellSizeKpc: float,
        n_mid: int,
        n_inner_region: int,
        n_outer_region: int,
        data3d: TurbulenceHeatingVazzaData3dReturnModel
    ) -> u.Quantity:
        '''
        rBoxKpc: The region you want to use to calculate total heating rate
        data3d: contain the turbulence heating data in the region bigger than rBoxKpc
        '''
        n_start_inner = n_mid - n_inner_region
        n_end_inner = n_mid + n_inner_region
        n_start_outer = n_mid - n_outer_region
        n_end_outer = n_mid + n_outer_region
        
        innerHeatingRatePerVolume: u.Quantity = \
            data3d.heatingPerVolume[n_start_inner:n_end_inner, n_start_inner:n_end_inner, n_start_inner:n_end_inner].mean()
        outerHeatingRatePerVolume: u.Quantity = \
            data3d.heatingPerVolume[n_start_outer:n_end_outer, n_start_outer:n_end_outer, n_start_outer:n_end_outer].mean()

        innerRegionVolume = u.Quantity(2*n_inner_region*cellSizeKpc, "kpc")**3
        outerRegionVolume = u.Quantity(2*n_outer_region*cellSizeKpc, "kpc")**3
        regionVolume = u.Quantity(2*rBoxKpc, "kpc")**3
        f = (regionVolume-innerRegionVolume)/(outerRegionVolume-innerRegionVolume)
        
        return (
            innerHeatingRatePerVolume*innerRegionVolume*(1-f) + \
            outerHeatingRatePerVolume*outerRegionVolume*f
        ).to("erg/s")
        
        
    
    def __getHeatingRateWithinSphereRegion(
        self,
        rKpc: float,
        cellSizeKpc: float,
        n_mid: int,
        n_inner_region: int,
        n_outer_region: int,
        data3d: TurbulenceHeatingVazzaData3dReturnModel
    ) -> u.Quantity:
        centerIndex = (n_mid, n_mid, n_mid)
        innerHeatingRatePerVolume = self.__getValidValueWithinSphereRegion(
            data3d.heatingPerVolume, centerIndex, n_inner_region).mean()
        outerHeatingRatePerVolume = self.__getValidValueWithinSphereRegion(
            data3d.heatingPerVolume, centerIndex, n_outer_region).mean()
        
        innerRegionVolume = (4./3.)*np.pi*(u.Quantity(n_inner_region*cellSizeKpc, "kpc")**3)
        outerRegionVolume = (4./3.)*np.pi*(u.Quantity(n_outer_region*cellSizeKpc, "kpc")**3)
        regionVolume = (4./3.)*np.pi*(u.Quantity(rKpc, "kpc")**3)
        f = (regionVolume-innerRegionVolume)/(outerRegionVolume-innerRegionVolume)

        return (
            innerHeatingRatePerVolume*innerRegionVolume*(1-f) + \
            outerHeatingRatePerVolume*outerRegionVolume*f
        ).to("erg/s")
    
    
    def __getValidValueWithinSphereRegion(
        self, 
        array: u.Quantity, 
        centerIndex: Tuple[int, int, int],
        radiusIndex: int
    ):
        # Calculate the distance of each index position
        x, y, z = np.indices(array.shape)
        coordinates = u.Quantity((x, y, z), unit=u.dimensionless_unscaled)
        target = u.Quantity(centerIndex, unit=u.dimensionless_unscaled)

        # Calculate the distance and convert to dimensionless quantity for comparison
        distances = np.sqrt(((coordinates[0] - target[0])**2 + 
                            (coordinates[1] - target[1])**2 + 
                            (coordinates[2] - target[2])**2)) * u.dimensionless_unscaled

        # Find the indices where the distance is less than 4 units
        mask = distances <= radiusIndex
        return array[mask]