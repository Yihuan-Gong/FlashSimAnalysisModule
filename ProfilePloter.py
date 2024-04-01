from typing import Tuple
from python.modules.Profile.CoolingTimeProfile import *
from python.modules.Profile.NoneCoolingGasPropertyProfile import *
from python.modules.Profile.TurbulenceHeatingProfile import *
from python.modules.GasProperty import GasProperty

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
    

    def selectProperty(self, gasProperty: GasProperty):
        if (gasProperty == GasProperty.Temperature or
            gasProperty == GasProperty.Pressure or
            gasProperty == GasProperty.Density or
            gasProperty == GasProperty.Entropy):
            self.profileStrategy = NoneCoolingGasPropertyProfile(self.basePath, gasProperty)
        elif (gasProperty == GasProperty.CoolingTime):
            self.profileStrategy = CoolingTimeProfile(self.basePath)
        elif (gasProperty == GasProperty.TurbulenceHeating):
            self.profileStrategy = TurbulenceHeatingProfile(self.basePath)
    

    def plot(self, timeMyr: float, ylim: Tuple[float, float]=None):
        self.profileStrategy.plot(timeMyr, ylim=ylim)

    
    def plotRange(self, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        self.profileStrategy.plotRange(startTimeMyr, endTimeMyr, stepMyr, ylim=ylim)