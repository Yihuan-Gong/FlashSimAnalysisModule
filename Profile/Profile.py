import abc
from typing import Tuple
# from python.modules.FieldAdder import FieldAdder

class Profile(metaclass=abc.ABCMeta):
    def __init__(self, basePath: str, myrPerFile=True):
        self.basePath = basePath
        self.myrPerFile = myrPerFile
        # FieldAdder.AddFields()

    @abc.abstractmethod
    def plot(self, timeMyr: float, ylim: Tuple[float, float]=None):
        pass
    
    @abc.abstractmethod
    def plotRange(self, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        pass
