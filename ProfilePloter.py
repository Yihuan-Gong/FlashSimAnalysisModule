from typing import Tuple
from .Profile.CoolingTimeProfile import *
from .Profile.NoneCoolingGasPropertyProfile import *
from .Profile.TurbulenceHeatingProfile import *
from .Enum.GasField import GasField
from .PandasHelper.PandasHelper import PandasHelper

''' 
    This class can only be used to plot
    1. Temperature profile
    2. Pressure profile
    3. Density profile
    4. Entropy profile
    5. Cooling time profile
'''

class ProfilePloter:
    def __init__(self, basePath) -> None:
        self.profileStrategy = None
        self.basePath = basePath
    

    def selectProperty(self, gasProperty: GasField):
        if (gasProperty == GasField.Temperature or
            gasProperty == GasField.Pressure or
            gasProperty == GasField.Density or
            gasProperty == GasField.Entropy):
            self.profileStrategy = NoneCoolingGasPropertyProfile(self.basePath, gasProperty)
        elif (gasProperty == GasField.CoolingTime):
            self.profileStrategy = CoolingTimeProfile(self.basePath)
        elif (gasProperty == GasField.TurbulenceHeating):
            self.profileStrategy = TurbulenceHeatingProfile(self.basePath)
    

    def plot(self, ax: plt.Axes, timeMyr: float, ylim: Tuple[float, float]=None):
        self.profileStrategy.plot(ax, timeMyr, ylim=ylim)

    
    def plotRange(self, ax: plt.Axes, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        self.profileStrategy.plotRange(ax, startTimeMyr, endTimeMyr, stepMyr, ylim=ylim)

    
    def resetDataBase(self, gasProperty: GasField):
        PandasHelper().resetDataBase(self.basePath, gasProperty)