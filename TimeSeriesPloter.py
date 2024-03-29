import matplotlib.pyplot as plt
from typing import Tuple
from python.modules.TimeSeries.GasPropertyTimeSeries import *
from python.modules.TimeSeries.JetPowerTimeSeries import *
from python.modules.TimeSeries.TurbulenceHeatingTimeSeries import *
from python.modules.GasProperty import GasProperty

class TimeSeriesPloter:
    def __init__(self, basePath) -> None:
        self.basePath = basePath
        self.timeSeriesStrategy = None

    
    def selectProperty(self, property: GasProperty, 
                       startTimeMyr: float, endTimeMyr: float, stepMyr: float,
                       myrPerFile: bool = True):
        if (property == GasProperty.Temperature or
            property == GasProperty.Pressure or
            property == GasProperty.Density or
            property == GasProperty.Entropy or
            property == GasProperty.Luminosity):
            self.timeSeriesStrategy = GasPropertyTimeSeries(
                self.basePath, property, startTimeMyr, endTimeMyr, stepMyr, myrPerFile
            )
        elif (property == GasProperty.JetPower):
            self.timeSeriesStrategy = JetPowerTimeSeries(
                self.basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile
            )
        elif (property == GasProperty.TurbulenceHeating):
            self.timeSeriesStrategy = TurbulenceHeatingTimeSeries(
                self.basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile
            )
    

    def plot(self, ax: plt.Axes, rKpc: float=None, ylim: Tuple[float, float]=None) -> plt.Axes:
        return self.timeSeriesStrategy.plot(ax, rKpc, ylim)
    

    def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
                  ylim: Tuple[float, float]=None) -> plt.Axes:
        return self.timeSeriesStrategy.plotRange(ax, rStartKpc, rEndKpc, rStepKpc, ylim)

