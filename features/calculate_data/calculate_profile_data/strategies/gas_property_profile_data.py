import yt
import numpy as np
# import concurrent.futures
# from multiprocessing import Pool
from typing import Tuple

from .profile_data import ProfileData
from ..data import DataModel
from ...utility import GasField, Shape, FieldAdder

'''
    This class can only be used to plot
    1. Temperature profile
    2. Pressure profile
    3. Density profile
    4. Entropy profile
'''

class GasPropertyProfileData(ProfileData):
    def __init__(self, gasProperty: GasField):
        super().__init__()
        FieldAdder.AddFields()
        self.gasProperty = gasProperty
        self.gasFieldName = self.__getFieldName()

    
    def getData(self) -> DataModel:
        if (self.shape == Shape.Box):
            raise ValueError("GasPropertyProfile only support Shape.Sphere")
        profile = self.__getProfile()
        return DataModel(
            x = np.array(profile.x).tolist(),
            value = np.array(profile[self.gasFieldName]).tolist(),
            label = (self.tMyr/1000, "Gyr")
        )
        
    
    def __getFieldName(self):
        if (self.gasProperty == GasField.Density):
            return ('gas', 'density')
        elif (self.gasProperty == GasField.Temperature):
            return ('gas', 'temp_in_keV')
        elif (self.gasProperty == GasField.Pressure):
            return ('gas', 'pressure')
        elif (self.gasProperty == GasField.Entropy):
            return ('gas', 'entropy')


    def __getProfile(self):
        ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, self.fileNum))
        sp = ds.sphere('c', (self.rEndKpc, 'kpc'))
        numberOfDatas = int((self.rEndKpc - self.rStartKpc)/self.rStepKpc)
        profile = yt.Profile1D(
            sp, ('gas', 'radius'), numberOfDatas, self.rStartKpc, self.rEndKpc, False, weight_field=('gas', 'mass')
        )
        profile.add_fields(self.gasFieldName)
        del ds
        del sp
        return profile
    

    # def __init__(self, basePath: str, gasProperty: GasField, myrPerFile:bool =True):
    #     super().__init__(basePath, myrPerFile)
    #     FieldAdder.AddFields()
    #     self.gasProperty = gasProperty
    #     self.gasFieldName = self.__getFieldName()


    # def plot(self, ax: plt.Axes, timeMyr: float, ylim: Tuple[float, float]=None):
    #     profile = self.__getProfile(timeMyr)
    #     self.__initPlot(ax, ylim)
    #     ax.plot(np.array(profile.x), np.array(profile[self.gasFieldName]), "-b", label="%.1f Gyr"%(timeMyr/1000))
    #     ax.legend()


    # def plotRange(self, ax: plt.Axes, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
    #               ylim: Tuple[float, float]=None):
    #     self.__initPlot(ax, ylim)
    #     for timeMyr in range(startTimeMyr, endTimeMyr, stepMyr):
    #         profile = self.__getProfile(timeMyr)
    #         ax.plot(np.array(profile.x), np.array(profile[self.gasFieldName]), label="%.1f Gyr"%(timeMyr/1000))
    #     ax.legend()
    

    # def __initPlot(self, ax: plt.Axes, ylim: Tuple[float, float]=None):        
    #     ax.set(xlabel='r $(kpc)$', xscale="log", yscale="log")
    #     if (self.gasProperty == GasField.Temperature):
    #         ax.set(
    #             ylabel='kT $(keV)$',
    #         )
    #     elif (self.gasProperty == GasField.Density):
    #         ax.set(
    #             ylabel='Density $(g/cm^3)$',
    #         )
    #     elif (self.gasProperty == GasField.Pressure):
    #         ax.set(
    #             ylabel='Pressure $(Ba)$',
    #         )
    #     elif (self.gasProperty == GasField.Entropy):
    #         ax.set(
    #             ylabel='S $(keV cm^2)$',
    #             ylim=(10, 1000),
    #         )
    #     if (ylim is not None):
    #         ax.set(ylim=ylim)
    
