import matplotlib.pyplot as plt
import yt
import numpy as np
from typing import Tuple
from python.modules.Profile.Profile import Profile
from python.modules.TurbulenceAnalyzor import TurbulenceAnalyzor

class TurbulenceHeatingProfile(Profile):
    def __init__(self, basePath: np.str, myrPerFile=True):
        super().__init__(basePath, myrPerFile)
        self.turbulenceAnalyzor = TurbulenceAnalyzor()


    def plot(self, timeMyr: float, ylim: Tuple[float, float]=None):
        rKpcStart = 50
        rKpcEnd = 300
        rStep = 25

        ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr))
        self.turbulenceAnalyzor.setDensityWeightingIndex(1).setDataSeries(ds)

        heatingRate = []
        rKpcs = range(rKpcStart, rKpcEnd, rStep)
        for rKpc in rKpcs:
            data = self.turbulenceAnalyzor.setBoxSize(rKpc).calculatePowerSpectrum().getDissipationRate()
            heatingRate.append(data['turb_heating_rate'])
        
        fig, ax = plt.subplots()
        ax.plot(rKpcs, heatingRate, label="%.2f Gyr"%(timeMyr/1000))
        ax.set_xlabel("t (Myr)")
        ax.set_ylabel("Power (erg/s)")
        ax.legend()



    def plotRange(self, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
                  ylim: Tuple[float, float]=None):
        pass


    


    
