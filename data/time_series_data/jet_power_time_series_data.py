import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple

from python.modules.data.data import DataModel

from .time_series_data import TimeSeriesData
from ...utility import Constants

class JetPowerTimeSeriesData(TimeSeriesData):
    __smoothingMyr: int = None
    __agnDataFileName: str = "perseus_merger_agn_0000000000000001.dat"

    def __init__(self) -> None:
        super().__init__()
    
    def setSmoothingMyr(self, smoothingMyr: int):
        self.__smoothingMyr = smoothingMyr


    def setAgnDataFileName(self, agnDataFileName):
        self.__agnDataFileName = agnDataFileName


    def getData(self) -> DataModel:
        fileName = self.__agnDataFileName
        header = pd.read_table(self.basePath + '/' + fileName, sep=', ', skiprows=[0], nrows=0, engine='python').columns
        datas = pd.read_table(self.basePath + '/' + fileName, sep="\s+", skiprows=[0,1], names=header)
        datas["Myr"] = datas['time (Myr)'] = datas['# time (s)']/Constants.Myr
        datas['jetpower (erg/s)'] = datas['energy (ergs)']/datas['dt(s)']
        filter1 = (datas['time (Myr)'] > self.tStartMyr)
        filter2 = (datas['time (Myr)'] < self.tEndMyr)
        filters = filter1 & filter2

        if (self.__smoothingMyr is not None):
            datas["MyrGroup"] = (datas["Myr"]//self.__smoothingMyr)
            groupedData = datas.groupby("MyrGroup").mean()
            return DataModel(
                x=groupedData['time (Myr)'].loc[filters].tolist(),
                value=groupedData['jetpower (erg/s)'].loc[filters].tolist(),
                label=None
            )
        
        return DataModel(
            x=datas['time (Myr)'].loc[filters].tolist(),
            value=datas['jetpower (erg/s)'].loc[filters].tolist(),
            label=None
        )
    
    
    
    # def __init__(self, basePath: str,
    #              startTimeMyr: float, endTimeMyr: float, stepMyr: float,
    #              myrPerFile: bool = True) -> None:
    #     super().__init__(basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile)
    #     self.solarMass = 1.9891e33
    #     self.Myr = 3.1557e13
    #     self.yr = 3.1557e7
    

    # def plot(self, ax: plt.Axes, rKpc: float = None, ylim: Tuple[float, float]=None) -> plt.Axes:
    #     if (ax is None):
    #         print("Please init plt.Axes before hand by fig, ax = plt.subplots()")
    #         return
    #     ax.set(
    #         xlabel="Time (Myr)", 
    #         ylabel="Power (erg/s)",
    #         ylim=ylim
    #     )

    #     fileName = 'perseus_merger_agn_0000000000000001.dat'
    #     header = pd.read_table(self.basePath + '/' + fileName, sep=', ', skiprows=[0], nrows=0, engine='python').columns
    #     datas = pd.read_table(self.basePath + '/' + fileName, sep="\s+", skiprows=[0,1], names=header)
    #     datas["Myr"] = datas['time (Myr)'] = datas['# time (s)']/self.Myr
    #     datas['jetpower (erg/s)'] = datas['energy (ergs)']/datas['dt(s)']

    #     groupStepMyr=20
    #     datas["MyrGroup"] = (datas["Myr"]//groupStepMyr)
    #     groupedData = datas.groupby("MyrGroup").mean()

    #     filter1 = (datas['time (Myr)'] > self.startTimeMyr)
    #     filter2 = (datas['time (Myr)'] < self.endTimeMyr)
    #     filters = filter1 & filter2

    #     ax.plot(datas['time (Myr)'].loc[filters], 
    #             datas['jetpower (erg/s)'].loc[filters],
    #             label="Heating", color="gray", alpha=0.5)
        
    #     ax.plot(groupedData['time (Myr)'].loc[filters], 
    #             groupedData['jetpower (erg/s)'].loc[filters],
    #             label="Average heating (%dMyr)"%groupStepMyr)
    #     ax.semilogy()
    #     ax.legend()
    #     return ax
    

    # def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
    #               ylim: Tuple[float, float]=None):
    #     print("Jet power doesn't support plot range")

    

