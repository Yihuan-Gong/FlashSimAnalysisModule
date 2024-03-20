from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from typing import Tuple

class TimeSeries(ABC):
    def __init__(self, basePath: str, startTimeMyr: float, endTimeMyr: float, 
                 stepMyr: float, myrPerFile: bool=True) -> None:
        self.basePath = basePath
        self.myrPerFile = myrPerFile
        self.startTimeMyr = startTimeMyr
        self.endTimeMyr = endTimeMyr
        self.stepMyr = stepMyr
        self.timesMyr = range(self.startTimeMyr, self.endTimeMyr, self.stepMyr)
    

    @abstractmethod
    def plot(self, ax: plt.Axes, rKpc: float, ylim: Tuple[float, float]=None) -> plt.Axes:
        pass
    
    
    @abstractmethod
    def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
                  ylim: Tuple[float, float]=None) -> plt.Axes:
        pass