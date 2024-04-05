import abc
import matplotlib.pyplot as plt
from typing import Tuple
from abc import ABC, abstractmethod
from ..PandasHelper.PandasHelper import PandasHelper

class Profile(ABC):
    def __init__(self, basePath: str, myrPerFile=True):
        self.basePath = basePath
        self.myrPerFile = myrPerFile
        self.pandasHelper = PandasHelper()

    @abstractmethod
    def plot(self, timeMyr: float, ylim: Tuple[float, float]=None):
        pass
    
    @abstractmethod
    def plotRange(self, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        pass
