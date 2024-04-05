import matplotlib.pyplot as plt
from typing import Tuple
from .TimeSeries.GasPropertyTimeSeries import *
from .TimeSeries.JetPowerTimeSeries import *
from .TimeSeries.TurbulenceHeatingTimeSeries import *
from .Enum.GasField import GasField

class TimeSeriesPloter:
    def __init__(self, basePath) -> None:
        self.basePath = basePath
        self.timeSeriesStrategy = None

    
    def selectProperty(self, property: GasField, 
                       startTimeMyr: float, endTimeMyr: float, stepMyr: float,
                       myrPerFile: bool = True):
        if (property == GasField.Temperature or
            property == GasField.Pressure or
            property == GasField.Density or
            property == GasField.Entropy or
            property == GasField.Luminosity):
            self.timeSeriesStrategy = GasPropertyTimeSeries(
                self.basePath, property, startTimeMyr, endTimeMyr, stepMyr, myrPerFile
            )
        elif (property == GasField.JetPower):
            self.timeSeriesStrategy = JetPowerTimeSeries(
                self.basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile
            )
        elif (property == GasField.TurbulenceHeating):
            self.timeSeriesStrategy = TurbulenceHeatingTimeSeries(
                self.basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile
            )
    

    def plot(self, ax: plt.Axes, rKpc: float=None, ylim: Tuple[float, float]=None) -> plt.Axes:
        return self.timeSeriesStrategy.plot(ax, rKpc, ylim)
    

    def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
                  ylim: Tuple[float, float]=None) -> plt.Axes:
        return self.timeSeriesStrategy.plotRange(ax, rStartKpc, rEndKpc, rStepKpc, ylim)
    
    def resetDataBase(self, property: GasField):
        PandasHelper().resetDataBase(self.basePath, property)


