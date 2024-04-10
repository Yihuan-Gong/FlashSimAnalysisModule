import yt
from typing import List

# from ..data_model import DataModel

from .profile_data import ProfileData
from ..data import DataModel
from ...analyzor.turbulence_analyzor import TurbulenceAnalyzor
from ...data_base import DataBaseModel
from ...utility import GasField

class TurbulenceHeatingProfileData(ProfileData):
    turbulenceAnalyzor: TurbulenceAnalyzor
    
    def __init__(self) -> None:
        super().__init__()
        self.turbulenceAnalyzor = TurbulenceAnalyzor()
        
    
    def getData(self) -> DataModel:
        return DataModel(
            x = self.r,
            value = self.__getProfile(),
            label = (self.tMyr/1000, "Gyr")
        )
    
    
    def __getProfile(self) -> List[float]:
        ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, self.fileNum))
        self.turbulenceAnalyzor.setDensityWeightingIndex(1).setDataSeries(ds)
        heatingRate = []
        for rKpc in self.r:
            value = self.pandasHelper.getDataFromCsv(self.basePath, GasField.TurbulenceHeating, rKpc, self.tMyr)
            if (value is not None):
                heatingRate.append(value)
                continue
            value = self.turbulenceAnalyzor.setBoxSize(rKpc).calculatePowerSpectrum().getDissipationRate()['turb_heating_rate']
            heatingRate.append(value)
            self.pandasHelper.writeDataIntoCsv(self.basePath, GasField.TurbulenceHeating, [DataBaseModel(rKpc, self.tMyr, value)])
        return heatingRate
    
    
    # def __init__(self, basePath: np.str, myrPerFile=True):
    #     super().__init__(basePath, myrPerFile)
    #     self.turbulenceAnalyzor = TurbulenceAnalyzor()
    #     self.rKpcStart = 50
    #     self.rKpcEnd = 300
    #     self.rStep = 25
    #     self.rKpcs = range(self.rKpcStart, self.rKpcEnd, self.rStep)


    # def plot(self, ax: plt.Axes, timeMyr: float, ylim: Tuple[float, float]=None):
    #     heatingRate = self.__getProfile(timeMyr)
    #     self.__initPlot(ax)
    #     ax.plot(self.rKpcs, heatingRate, label="%.2f Gyr"%(timeMyr/1000))
    #     ax.legend()



    # def plotRange(self, ax: plt.Axes, startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
    #               ylim: Tuple[float, float]=None):
    #     self.__initPlot(ax)
    #     for timeMyr in range(startTimeMyr, endTimeMyr, stepMyr):
    #         heatingRate = self.__getProfile(timeMyr)
    #         ax.plot(self.rKpcs, heatingRate, label="%.2f Gyr"%(timeMyr/1000))
    #     ax.legend()


    # def __initPlot(self, ax: plt.Axes):
    #     ax.set_xlabel("t (Myr)")
    #     ax.set_ylabel("Power (erg/s)")

    
    
        


    


    
