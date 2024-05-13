from typing import Iterable, Tuple
import matplotlib.pyplot as plt

from ..models import Plot1dInfoModel
from ....calculate_data.calculate_data1d import (
    ProfileReturnModel,
    TimeSeriesReturnModel,
    TurbulenceHeatingProfileReturnModel,
    TurbulenceHeatingTimeSeriesReturnModel
)


class Plot1dRenderer:
    
    def renderProfilePlot(
        self,
        data: ProfileReturnModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        
        if (plotInfo.xLabel == "default"):
            plotInfo.xLabel = "kpc"
        if (plotInfo.yLabel == "default"):
            plotInfo.yLabel = data.yValue.unit.to_string()
        if plotInfo.lineLabel == "default":
            plotInfo.lineLabel = f"{data.timeMyr} Myr"
        
        return self.__renderPlot1d(
            xValue=data.rKpcList,
            yValue=data.yValue.value,
            plotInfo=plotInfo
        )
        
    
    def renderTimeSeriesPlot(
        self,
        data: TimeSeriesReturnModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        
        if (plotInfo.xLabel == "default"):
            plotInfo.xLabel = "Myr"
        if (plotInfo.yLabel == "default"):
            plotInfo.yLabel = data.yValue.unit.to_string()
        if plotInfo.lineLabel == "default":
            plotInfo.lineLabel = f"{data.rKpc} kpc"
        
        return self.__renderPlot1d(
            xValue=data.timeMyrList,
            yValue=data.yValue.value,
            plotInfo=plotInfo
        )
    
    
    def renderFillBetweenProfilePlot(
        self,
        data: TurbulenceHeatingProfileReturnModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        
        if (plotInfo.xLabel == "default"):
            plotInfo.xLabel = "kpc"
        if (plotInfo.yLabel == "default"):
            plotInfo.yLabel = data.lowerLimit.unit.to_string()
        if plotInfo.lineLabel == "default":
            plotInfo.lineLabel = f"{data.timeMyr} Myr"
        
        return self.__renderFillBetweenPlot1d(
            xValue=data.rKpcList,
            yLowerValue=data.lowerLimit.value,
            yUpperValue=data.upperLimit.value,
            plotInfo=plotInfo
        )
    
    
    def renderFillBetweenTimeSeries(
        self,
        data: TurbulenceHeatingTimeSeriesReturnModel,
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        
        if (plotInfo.xLabel == "default"):
            plotInfo.xLabel = "Myr"
        if (plotInfo.yLabel == "default"):
            plotInfo.yLabel = data.lowerLimit.unit.to_string()
        if plotInfo.lineLabel == "default":
            plotInfo.lineLabel = f"{data.rKpc} kpc"
        
        return self.__renderFillBetweenPlot1d(
            xValue=data.timeMyrList,
            yLowerValue=data.lowerLimit.value,
            yUpperValue=data.upperLimit.value,
            plotInfo=plotInfo
        )
    
    
    def __renderPlot1d(
        self,
        xValue: Iterable[float],
        yValue: Iterable[float],
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        
        if (plotInfo.fig == None or plotInfo.ax == None):
            plotInfo.fig, plotInfo.ax = plt.subplots()

        line = plotInfo.ax.plot(
            xValue, yValue, label=plotInfo.lineLabel, alpha=plotInfo.lineAlpha)
        if (plotInfo.lineColor != "default"):
            line[0].set_color(plotInfo.lineColor)
        if (plotInfo.lineStyle != "default"):
            line[0].set_linestyle(plotInfo.lineStyle)
            
        self.__setPlot1dAxes(plotInfo)
        return plotInfo.fig, plotInfo.ax
    
    
    def __renderFillBetweenPlot1d(
        self,
        xValue: Iterable[float],
        yUpperValue: Iterable[float],
        yLowerValue: Iterable[float],
        plotInfo: Plot1dInfoModel
    ) -> Tuple[plt.Figure, plt.Axes]:
        
        if (plotInfo.fig == None or plotInfo.ax == None):
            plotInfo.fig, plotInfo.ax = plt.subplots()

        polyCollection = plotInfo.ax.fill_between(
            xValue, yLowerValue, yUpperValue, 
            label=plotInfo.lineLabel, alpha=plotInfo.lineAlpha
        )
        if (plotInfo.lineColor != "default"):
            polyCollection.set_color(plotInfo.lineColor)
        
        self.__setPlot1dAxes(plotInfo)
        return plotInfo.fig, plotInfo.ax
    
    
    def __setPlot1dAxes(self, plotInfo: Plot1dInfoModel):
        plotInfo.ax.set_xlabel(plotInfo.xLabel)
        plotInfo.ax.set_ylabel(plotInfo.yLabel)
        plotInfo.ax.set_title(plotInfo.title)
        plotInfo.ax.set_xbound(plotInfo.xLowerBound, plotInfo.xUpperBound)
        plotInfo.ax.set_ybound(plotInfo.yLowerBound, plotInfo.yUpperBound)
        if (plotInfo.showLegend):
            plotInfo.ax.legend()
        if (plotInfo.xLogScale):
            plotInfo.ax.semilogx()
        if (plotInfo.yLogScale):
            plotInfo.ax.semilogy()

