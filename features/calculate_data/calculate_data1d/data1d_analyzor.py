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
    TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel,
    TurbulenceHeatingVazzaProfileCalculationInfoModel
)
from .methods.yt import (
    YtData1d,
    YtProfileCalculationInfoModel,
    YtTimeSeriesCalculationInfoModel,
)
from .methods.xray import (
    XrayData1d,
    XrayProfileCalculationInfoModel,
    XrayTimeSeriesCalculationInfoModel
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
    
    
    def turbulenceHeatingVazzaProfile(
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
        return TurbulenceHeatingVazzaData1d().getProfile(
            powerMode=powerMode,
            turbMode=turbMode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def turbulenceHeatingVazzaTimeSeries(
        self,
        powerMode: str,
        turbMode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        '''
        powerMode: "total" or "perVolume"
        '''
        return TurbulenceHeatingVazzaData1d().getTimeSeries(
            powerMode=powerMode,
            turbMode=turbMode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
    
    
    def ytProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: YtProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        '''
        Profile doesn't support Shape.Box
        '''
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
    
    
    def xrayProfile(
        self, 
        mode: str,
        simFile: SimFileModel,
        calculationInfo: XrayProfileCalculationInfoModel
    ) -> ProfileReturnModel:
        '''
        mode: "emissivity" or "luminosity"
        
        This "luminosity" mode automatically do volume intergral from the result of
        "emissivity" mode. So please use smaller rStepKpc. The smaller rStepKpc
        is, the more accurate the result is. Using smaller rStepKpc will not result in longer
        runtime, since the bottom of this method is yt.Profile1D
        
        Profile doesn't support Shape.Box
        '''
        if (mode == "emissivity"):
            return XrayData1d().getXrayEmissivityProfile(
                simFile=simFile,
                calculationInfo=calculationInfo
            )
        else:
            return XrayData1d().getXrayLuminosityProfile(
                simFile=simFile,
                calculationInfo=calculationInfo
            )
    
    
    def xrayTimeSeries(
        self,
        mode: str,
        simFile: SimFileModel,
        calculationInfo: XrayTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        '''
        mode: "emissivity" or "luminosity"
        '''
        if (mode == "emissivity"):
            return XrayData1d().getXrayEmissivityTimeSeries(
                simFile=simFile,
                calculationInfo=calculationInfo
            )
        else:
            return XrayData1d().getXrayLuminosityTimeSeries(
                simFile=simFile,
                calculationInfo=calculationInfo
            )
    
    

