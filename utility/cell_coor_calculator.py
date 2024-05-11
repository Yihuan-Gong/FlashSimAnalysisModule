from astropy import units as u
from typing import TypeVar

from ..services import YtRawDataHelper
from ..models import SimFileModel
from ..models.interfaces import (
    DataNdCalculationInfoModel,
    CoordinateModel
)

class CellCoorCalculator:
    T = TypeVar('T')
    
    def getAxisCoor(self, simFile: SimFileModel, calculationInfo: T)\
        -> u.Quantity:
        '''
        Extract the coordinate for x axis within rBoxKpc,
        which can also be applied to y and z axis since the rBoxKpc domain is a cube
        
        Inputs:
            simFile: SimFileModel
            calculationInfo: Generic type that implement DataNdCalculationInfoModel and CoordinateModel
        
        Output:
            u.Quantity: The coordinate for x axis within rBoxKpc
        '''
        if isinstance(calculationInfo, DataNdCalculationInfoModel) and \
           isinstance(calculationInfo, CoordinateModel):
            return YtRawDataHelper().loadRawData(
                simFile=simFile,
                timeMyr=calculationInfo.timeMyr,
                rBoxKpc=calculationInfo.rBoxKpc,
                fields=[calculationInfo.cellCoorField]
            )[0][calculationInfo.cellCoorField]\
                .in_units(calculationInfo.cellCoorUnit)[:,0,0].to_astropy()
        else:
            raise ValueError(
                "calculation info should implement DataNdCalculationInfoModel and CoordinateModel"
            )
                
    