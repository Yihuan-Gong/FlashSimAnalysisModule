import matplotlib.pyplot as plt
import yt
import numpy as np
import concurrent.futures
# from multiprocessing import Pool
from typing import Tuple
from .Profile import Profile
from ..Enum.GasField import GasField
from ..FieldAdder import FieldAdder

'''
    This class can only be used to plot
    1. Temperature profile
    2. Pressure profile
    3. Density profile
    4. Entropy profile
'''

class NoneCoolingGasPropertyProfile(Profile):
    def __init__(self, basePath: str, gasProperty: GasField, myrPerFile:bool =True):
        super().__init__(basePath, myrPerFile)
        FieldAdder.AddFields()
        self.gasProperty = gasProperty
        self.gasFieldName = self.__getFieldName()


    def plot(self, ax: plt.Axes, timeMyr: float, ylim: Tuple[float, float]=None):
        profile = self.__getProfile(timeMyr)
        self.__initPlot(ax, ylim)
        ax.plot(np.array(profile.x), np.array(profile[self.gasFieldName]), "-b", label="%.1f Gyr"%(timeMyr/1000))
        ax.legend()


    def plotRange(self, ax: plt.Axes, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        self.__initPlot(ax, ylim)
        for timeMyr in range(startTimeMyr, endTimeMyr, stepMyr):
            profile = self.__getProfile(timeMyr)
            ax.plot(np.array(profile.x), np.array(profile[self.gasFieldName]), label="%.1f Gyr"%(timeMyr/1000))
        ax.legend()


    def __getFieldName(self):
        if (self.gasProperty == GasField.Density):
            return ('gas', 'density')
        elif (self.gasProperty == GasField.Temperature):
            return ('gas', 'temp_in_keV')
        elif (self.gasProperty == GasField.Pressure):
            return ('gas', 'pressure')
        elif (self.gasProperty == GasField.Entropy):
            return ('gas', 'entropy')


    def __getProfile(self, timeMyr: float):
        ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr))
        sp = ds.sphere('c', (1, 'Mpc'))
        profile = yt.Profile1D(
            sp, ('gas', 'radius'), 64, 1, 1000, False, weight_field=('gas', 'mass')
        )
        profile.add_fields(self.gasFieldName)
        del ds
        del sp
        return profile
    

    def __initPlot(self, ax: plt.Axes, ylim: Tuple[float, float]=None):        
        ax.set(xlabel='r $(kpc)$', xscale="log", yscale="log")
        if (self.gasProperty == GasField.Temperature):
            ax.set(
                ylabel='kT $(keV)$',
            )
        elif (self.gasProperty == GasField.Density):
            ax.set(
                ylabel='Density $(g/cm^3)$',
            )
        elif (self.gasProperty == GasField.Pressure):
            ax.set(
                ylabel='Pressure $(Ba)$',
            )
        elif (self.gasProperty == GasField.Entropy):
            ax.set(
                ylabel='S $(keV cm^2)$',
                ylim=(10, 1000),
            )
        if (ylim is not None):
            ax.set(ylim=ylim)
    
