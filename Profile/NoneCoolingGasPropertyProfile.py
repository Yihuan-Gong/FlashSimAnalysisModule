import matplotlib.pyplot as plt
import yt
import numpy as np
import concurrent.futures
# from multiprocessing import Pool
from typing import Tuple
from python.modules.Profile.Profile import Profile
from python.modules.Enum.GasField import GasField
from python.modules.FieldAdder import FieldAdder

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
        self.gasField = self.__getFieldName()


    # overriding abstract method
    def plot(self, timeMyr: float, ylim: Tuple[float, float]=None):
        profile = self.__getProfile(timeMyr)
        ax = self.__initPlot(ylim)
        ax.plot(np.array(profile.x), np.array(profile[self.gasField]), "-b", label="%.1f Gyr"%(timeMyr/1000))
        ax.legend()


    # overriding abstract method
    def plotRange(self, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        ax = self.__initPlot(ylim)
        for timeMyr in range(startTimeMyr, endTimeMyr, stepMyr):
            profile = self.__getProfile(timeMyr)
            ax.plot(np.array(profile.x), np.array(profile[self.gasField]), label="%.1f Gyr"%(timeMyr/1000))
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
        profile.add_fields(self.gasField)
        del ds
        del sp
        return profile
    

    def __initPlot(self, ylim: Tuple[float, float]=None):
        fig, ax = plt.subplots()
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
        
        return ax
    

    # with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        #     # Create a list of futures for parallel execution
        #     futures = [executor.submit(self.__getProfile, timeMyr) 
        #                for timeMyr in range(startTimeMyr, endTimeMyr, stepMyr)]
        #     print("Finished submit")

        #     concurrent.futures.wait(futures)
        #     print("Finished results")

        #     for future in futures:
        #         try:
        #             profile, timeMyr = future.result()
        #             ax.plot(np.array(profile.x), np.array(profile[self.gasField]), label="%.1f Gyr"%(timeMyr/1000))
        #         except Exception as e:
        #             print(f"Error: {e}")
    
