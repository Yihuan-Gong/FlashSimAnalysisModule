from typing import Tuple
import matplotlib.pyplot as plt

from .models import Plot1dInfoModel
from .utilities import Plot1dRenderer
from ...calculate_data.calculate_data1d import *


class Plot1d:
    
    def jetPowerTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: JetPowerTimeSeriesCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        data = Data1dAnalyzor().jetPowerTimeSeries(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderTimeSeriesPlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def turbulenceHeatingProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingProfileCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        data = Data1dAnalyzor().turbulenceHeatingProfile(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderFillBetweenProfilePlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def turbulenceHeatingTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingTimeSeriesCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        data = Data1dAnalyzor().turbulenceHeatingTimeSeries(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderFillBetweenTimeSeries(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def turbulenceHeatingVazzaProfile(
        self,
        powerMode: str,
        turbMode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaProfileCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        '''
        powerMode: "total" or "perVolume"
        
        If you use mode "total", this method automatically to volume integral
        from the result of mode "perVolume" Therefore, to ensure a accurate result
        and get rid of intergration constant error, please set rKpcStart=0 and use
        lower rStepKpc.
        
        Shape.Box is not supported. Please set shape=Shape.Sphere at calculationInfo: 
        TurbulenceHeatingVazzaProfileCalculationInfoModel.
        '''
        data = Data1dAnalyzor().turbulenceHeatingVazzaProfile(
            powerMode=powerMode,
            turbMode=turbMode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderProfilePlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def turbulenceHeatingVazzaTimeSeries(
        self,
        powerMode: str,
        turbMode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        '''
        powerMode: "total" or "perVolume"
        '''
        data = Data1dAnalyzor().turbulenceHeatingVazzaTimeSeries(
            powerMode=powerMode,
            turbMode=turbMode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderTimeSeriesPlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    
    def ytProfile(
        self,
        simFile: SimFileModel,
        calculationInfo: YtProfileCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        data = Data1dAnalyzor().ytProfile(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderProfilePlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def ytTimeSeries(
        self,
        simFile: SimFileModel,
        calculationInfo: YtTimeSeriesCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        data = Data1dAnalyzor().ytTimeSeries(
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderTimeSeriesPlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def xrayProfile(
        self,
        mode: str,
        simFile: SimFileModel,
        calculationInfo: XrayProfileCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        '''
        mode: "emissivity" or "luminosity"
        
        This "luminosity" mode automatically do volume intergral from the result of
        "emissivity" mode. So please use smaller rStepKpc. The smaller rStepKpc
        is, the more accurate the result is. Using smaller rStepKpc will not result in longer
        runtime, since the bottom of this method is yt.Profile1D
        
        Profile doesn't support Shape.Box
        '''
        data = Data1dAnalyzor().xrayProfile(
            mode=mode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderProfilePlot(
            data=data,
            plotInfo=plotInfo
        )
    
    
    def xrayTimeSeries(
        self,
        mode: str,
        simFile: SimFileModel,
        calculationInfo: XrayTimeSeriesCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        '''
        mode: "emissivity" or "luminosity"
        '''
        data = Data1dAnalyzor().xrayTimeSeries(
            mode=mode,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Plot1dRenderer().renderTimeSeriesPlot(
            data=data,
            plotInfo=plotInfo
        )

    