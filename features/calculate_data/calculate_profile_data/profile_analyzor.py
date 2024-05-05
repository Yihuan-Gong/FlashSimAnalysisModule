from .strategies import *
from .enums.profile_mode import ProfileMode
from .models import ProfileCalculationInfoModel
from ....models.data1d_return_model.data1d_return_model import Data1dReturnModel
from ....models.sim_file_model import SimFileModel

class ProfileAnalyzor:
    __profileStrategy : ProfileData
    
    
    def setInputs(self, profileMode: ProfileMode, simFile: SimFileModel,
                 calculationInfo: ProfileCalculationInfoModel):
        className = f"{profileMode}".split(".")[-1] + ProfileData.__name__
        self.__profileStrategy = globals()[className]()
        self.__profileStrategy.setInputs(simFile, calculationInfo)
        return self
    
    
    def getData(self) -> Data1dReturnModel:
        return self.__profileStrategy.getData()
    

    