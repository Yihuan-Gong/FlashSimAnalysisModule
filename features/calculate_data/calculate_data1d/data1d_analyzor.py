from .methods.jet_power import (
    JetPowerData1d,
    JetPowerTimeSeriesCalculationInfoModel
)
from .methods.turbulence_heating import (
    TurbulenceHeatingData1d,
    TurbulenceHeatingProfileCalculationInfoModel,
    TurbulenceHeatingTimeSeriesCalculationInfoModel,
    TurbulenceHeatingProfileReturnModel,
    TurbulenceHeatingTimeSeriesReturnModel
    
)
from .methods.turbulence_heating_vazza import (
    TurbulenceHeatingVazzaData1d,
    TurbulenceHeatingVazzaMode,
    TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
)
from .methods.yt import (
    YtData1d,
    YtProfileCalculationInfoModel,
    YtTimeSeriesCalculationInfoModel,
)
from .models import (
    ProfileReturnModel,
    TimeSeriesReturnModel
)
from ....models import SimFileModel


class Data1dAnalyzor:
    
    def jetPowerTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: JetPowerTimeSeriesCalculationInfoModel,
    ) -> TimeSeriesReturnModel:
        return JetPowerData1d().getTimeSeriesData(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def turbulenceHeatingProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingProfileCalculationInfoModel
    ) -> TurbulenceHeatingProfileReturnModel:
        return TurbulenceHeatingData1d().getProfileData(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def turbulenceHeatingTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingTimeSeriesCalculationInfoModel
    ) -> TurbulenceHeatingTimeSeriesReturnModel:
        return TurbulenceHeatingData1d().getTimeSeriesData(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def turbulenceHeatingVazzaTimeSeries(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        return TurbulenceHeatingVazzaData1d().getTimeSeries(
            mode=mode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def ytProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: YtProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        return YtData1d().getProfileData(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def ytTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: YtTimeSeriesCalculationInfoModel,
    ) -> TimeSeriesReturnModel:
        return YtData1d().getTimeSeries(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    

