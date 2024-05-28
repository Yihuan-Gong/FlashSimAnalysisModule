from .models import (
    TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel,
    TurbulenceHeatingVazzaProfileCalculationInfoModel
)
from .methods import (
    TurbulenceHeatingVazzaProfile,
    TurbulenceHeatingVazzaTimeSeries
)
from ...models import (
    ProfileReturnModel,
    TimeSeriesReturnModel
)
from ....calculate_data3d import (
    TurbulenceHeatingVazzaMode,
)
from ......models import SimFileModel


class TurbulenceHeatingVazzaData1d:
    
    def getTimeSeries(
        self,
        powerMode: str,
        turbMode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        '''
        powerMode: "total" or "perVolume"
        '''
        return TurbulenceHeatingVazzaTimeSeries().getTimeSeries(
            powerMode=powerMode,
            turbMode=turbMode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        
    
    def getProfile(
        self,
        powerMode: str,
        turbMode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        '''
        powerMode: "total" or "perVolume"
        
        If you use mode "total", this method automatically to volume integral
        from the result of mode "perVolume" Therefore, to ensure a accurate result
        and get rid of intergration constant error, please set rKpcStart=0 and use
        lower rStepKpc.
        
        Please also use smaller rStepKpc for mode "perVolume", because it make the
        curve smoother and take the same time as larger rStepKpc.
        
        Shape.Box is not supported
        '''
        return TurbulenceHeatingVazzaProfile().getProfile(
            powerMode=powerMode,
            turbMode=turbMode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    