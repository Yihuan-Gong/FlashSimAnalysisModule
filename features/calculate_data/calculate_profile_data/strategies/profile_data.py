import matplotlib.pyplot as plt
from typing import List

from ..data import Data, DataModel
from .....data_base import *

class ProfileData(Data):
    rStartKpc: float
    rEndKpc: float
    rStepKpc: float
    r: List[float]
    tMyr: float
    
    def __init__(self) -> None:
        super().__init__()


    def setRadiusSpanKpc(self, rStartKpc: float, rEndKpc: float, rStepKpc: float):
        self.rStartKpc = rStartKpc
        self.rEndKpc = rEndKpc
        self.rStepKpc = rStepKpc
        self.r = range(self.rStartKpc, self.rEndKpc, self.rStepKpc)
        return self
    
    
    def setTimeMyr(self, tMyr: float):
        self.tMyr = tMyr
        self.fileNum = int(self.tMyr/self.fileStepMyr)
        return self


    def getData(self) -> DataModel:
        raise NotImplementedError("Please use the sub-class, such as CoolingTimeProfile")
    


    # def __init__(self, basePath: str, myrPerFile=True):
    #     self.basePath = basePath
    #     self.myrPerFile = myrPerFile
    #     self.pandasHelper = PandasHelper()

    # @abstractmethod
    # def plot(self, timeMyr: float, ylim: Tuple[float, float]=None):
    #     pass
    
    # @abstractmethod
    # def plotRange(self, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
    #               ylim: Tuple[float, float]=None):
    #     pass
