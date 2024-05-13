from typing import Dict, List, Tuple
from astropy import units as u

from ......enum import Shape

class XAxisAndLabel:
    '''
    The unit of xValue will be set to the following value by default
    kpc for mode="profile".
    Myr for mode="ts".
    So no unit when set xValue.
    '''
    __rUnit = 1*u.Unit("kpc")
    __tUnit = 1*u.Unit("Myr")
    __timeLabel = "t"
    __xValue: List[float]
    __shape: Shape
    __mode: str
    __lineLabel: float
    
    def __init__(
        self, 
        xValueWithoutUnit: List[float], 
        shape: Shape, 
        mode: str, 
        lineLabel: float
    ) -> None:
        self.__xValue = xValueWithoutUnit
        self.__shape = shape
        self.__mode = mode
        self.__lineLabel = lineLabel
    
    
    def getxValue(self):
        if (self.__mode == "profile"):
            return self.__xValue*self.__rUnit
        else:
            return self.__xValue*self.__tUnit
    
    
    def getxLabel(self):
        if (self.__mode == "profile"):
            return self.__getrLabel()
        else:
            return self.__timeLabel
    
    
    def getLineLabel(self) -> Tuple[str, u.Quantity]:
        if (self.__lineLabel == None):
            return None
        if (self.__mode == "profile"):
            return (self.__timeLabel, self.__lineLabel*self.__tUnit)
        else:
            return (self.__getrLabel(), self.__lineLabel*self.__rUnit)
        
    
    def __getrLabel(self) -> str:
        if (self.__shape == Shape.Box):
            return "rBox"
        elif (self.__shape == Shape.Sphere):
            return "r"
        else:
            return None