import yt
from typing import List

from .profile_data import ProfileData
from ..data_model import DataModel
from ..turb_data_model import TurbDataModel
from ...analyzor.turbulence_analyzor import TurbulenceAnalyzor
from ...data_base import TurbPandasHelper, DbModel, TurbDbModel
from ...utility import GasField, Shape

class TurbulenceHeatingProfileData(ProfileData):
    turbulenceAnalyzor: TurbulenceAnalyzor
    turbPandasHelper: TurbPandasHelper
    rhoIndex: float = None
    
    def __init__(self) -> None:
        super().__init__()
        self.turbulenceAnalyzor = TurbulenceAnalyzor()
        self.turbPandasHelper = TurbPandasHelper()
    

    def setRhoIndex(self, rhoIndex: float):
        self.rhoIndex = rhoIndex
    
    def getData(self) -> DataModel:
        if (self.shape != Shape.Box):
            raise ValueError("Turbulence heating only support box shape!")
        if (self.rhoIndex is None):
            raise ValueError("You must set the rho index")
        return DataModel(
            x = self.r,
            value = self.__getProfile(),
            label = (self.tMyr/1000, "Gyr")
        )
    
    
    def __getProfile(self) -> TurbDataModel:
        turbDataList: List[TurbDbModel] = []
        for rKpc in self.r:
            turbData = self.turbPandasHelper.getTurbDataFromCsv(
                self.basePath,
                self.shape,
                rKpc,
                self.tMyr,
                self.rhoIndex
            )
            if (turbData is not None):
                turbDataList.append(turbData)
                continue
            
            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, self.fileNum))
            turbDataTemp = self.turbulenceAnalyzor \
                            .setDensityWeightingIndex(self.rhoIndex) \
                            .setDataSeries(ds) \
                            .setBoxSize(rKpc) \
                            .calculatePowerSpectrum() \
                            .getDissipationRate()
            turbData = TurbDbModel(
                rhoIndex=self.rhoIndex,
                upperLimit=turbDataTemp["turb_heating_rate_upper_limit"],
                lowerLimit=turbDataTemp["turb_heating_rate_lower_limit"]
            )
            turbDataList.append(turbData)
            self.pandasHelper.writeDataIntoCsv(
                self.basePath,
                GasField.TurbulenceHeating, 
                self.shape,
                [DbModel(rKpc=rKpc, tMyr=self.tMyr, value=turbData)]
            )

        return TurbDataModel(
            rhoIndex=self.rhoIndex,
            upperLimit=[x.upperLimit for x in turbDataList],
            lowerLimit=[x.lowerLimit for x in turbDataList]
        )
    
    
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

    
    
        


    


    
