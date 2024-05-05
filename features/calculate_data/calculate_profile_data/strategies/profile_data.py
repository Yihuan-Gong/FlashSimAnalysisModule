from ..models import *
from .....models import Data1dReturnModel, SimFileModel
from .....data_base import *

class ProfileData:
    _simFile: SimFileModel
    _calculationInfo: ProfileCalculationInfoModel
    _r: range
    
    
    def setInputs(self, simFile: SimFileModel, calculationInfo: ProfileCalculationInfoModel):
        self._simFile = simFile
        self._calculationInfo = calculationInfo
        self._r = range(
            self._calculationInfo.rStartKpc, 
            self._calculationInfo.rEndKpc,
            self._calculationInfo.rStepKpc
        )


    def getData(self) -> Data1dReturnModel:
        raise NotImplementedError("Please use the sub-class, such as CoolingTimeProfile")
    