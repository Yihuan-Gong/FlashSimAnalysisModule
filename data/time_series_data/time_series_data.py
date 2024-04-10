import matplotlib.pyplot as plt
from typing import Tuple, List

from ..data import Data, DataModel

class TimeSeriesData(Data):
    tStartMyr: float
    tEndMyr: float
    tStepMyr: float
    t: List[float]
    fileNums: List[int]
    rKpc: float

    def __init__(self) -> None:
        super().__init__()

    
    def setTimeSpanMyr(self, tStartMyr: float, tEndMyr: float, tStepMyr: float):
        self.tStartMyr = tStartMyr
        self.tEndMyr = tEndMyr
        self.tStepMyr = tStepMyr
        self.t = range(self.tStartMyr, self.tEndMyr, self.tStepMyr)
        self.fileNums = [int(x/self.fileStepMyr) for x in self.t]

    
    def setRadiusKpc(self, rKpc: float):
        self.rKpc = rKpc

    
    def getData(self) -> DataModel:
        raise NotImplementedError("Please use the sub-class, such as GasPropertyTimeSeriesData")



    # def __init__(self, basePath: str, startTimeMyr: float, endTimeMyr: float, 
    #              stepMyr: float, myrPerFile: bool=True) -> None:
    #     self.basePath = basePath
    #     self.myrPerFile = myrPerFile
    #     self.startTimeMyr = startTimeMyr
    #     self.endTimeMyr = endTimeMyr
    #     self.stepMyr = stepMyr
    #     self.timesMyr = range(self.startTimeMyr, self.endTimeMyr, self.stepMyr)
    

    # @abstractmethod
    # def plot(self, ax: plt.Axes, rKpc: float, ylim: Tuple[float, float]=None) -> plt.Axes:
    #     pass
    
    
    # @abstractmethod
    # def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
    #               ylim: Tuple[float, float]=None) -> plt.Axes:
    #     pass