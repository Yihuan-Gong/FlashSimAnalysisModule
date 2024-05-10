from .enums import TurbulenceHeatingVazzaMode
from .models import (
    TurbulenceHeatingVazzaData2dReturnModel,
    TurbulenceHeatingVazzaData3dReturnModel,
    TurbulenceHeatingVazzaCalculationInfoModel
)
from .strategies import (
    TurbulenceHeatingVazzaStrategy,
    TurbVelTurbulenceHeatingVazzaStrategy
)
from .....models import SimFileModel


class TurbulenceHeatingVazza:
    __strategy: TurbulenceHeatingVazzaStrategy
    
    def setInputs(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    ):
        className: str = f"{mode}".split(".")[-1] + TurbulenceHeatingVazzaStrategy.__name__
        self.__strategy = globals()[className]()
        self.__strategy.setInputs(simFile, calculationInfo)
        return self
    
    
    def getData2d(self, axis: str) -> TurbulenceHeatingVazzaData2dReturnModel:
        return self.__strategy.getData2d(axis)
    
    
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        return self.__strategy.getData3d()
    

