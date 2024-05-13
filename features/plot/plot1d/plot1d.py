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
    
    
    
    def turbulenceHeatingVazzaTimeSeries(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaTimeSeriesCalculationInfoModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        data = Data1dAnalyzor().turbulenceHeatingVazzaTimeSeries(
            mode=mode,
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
    
    

        
        
    
    