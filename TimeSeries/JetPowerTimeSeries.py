import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple
from python.modules.TimeSeries.TimeSeries import TimeSeries

class JetPowerTimeSeries(TimeSeries):
    def __init__(self, basePath: str,
                 startTimeMyr: float, endTimeMyr: float, stepMyr: float,
                 myrPerFile: bool = True) -> None:
        super().__init__(basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile)
        self.solarMass = 1.9891e33
        self.Myr = 3.1557e13
        self.yr = 3.1557e7
    

    def plot(self, ax: plt.Axes, rKpc: float = None, ylim: Tuple[float, float]=None) -> plt.Axes:
        if (ax is None):
            print("Please init plt.Axes before hand by fig, ax = plt.subplots()")
            return
        ax.set(
            xlabel="Time (Myr)", 
            ylabel="Power (erg/s)",
            ylim=ylim
        )

        fileName = 'perseus_merger_agn_0000000000000001.dat'
        header = pd.read_table(self.basePath + '/' + fileName, sep=', ', skiprows=[0], nrows=0, engine='python').columns
        datas = pd.read_table(self.basePath + '/' + fileName, sep="\s+", skiprows=[0,1], names=header)
        datas["Myr"] = datas['time (Myr)'] = datas['# time (s)']/self.Myr
        datas['jetpower (erg/s)'] = datas['energy (ergs)']/datas['dt(s)']

        groupStepMyr=20
        datas["MyrGroup"] = (datas["Myr"]//groupStepMyr)
        groupedData = datas.groupby("MyrGroup").mean()

        filter1 = (datas['time (Myr)'] > self.startTimeMyr)
        filter2 = (datas['time (Myr)'] < self.endTimeMyr)
        filters = filter1 & filter2

        ax.plot(datas['time (Myr)'].loc[filters], 
                datas['jetpower (erg/s)'].loc[filters],
                label="Heating", color="gray", alpha=0.5)
        
        ax.plot(groupedData['time (Myr)'].loc[filters], 
                groupedData['jetpower (erg/s)'].loc[filters],
                label="Average heating (%dMyr)"%groupStepMyr)
        ax.semilogy()
        ax.legend()
        return ax
    

    def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
                  ylim: Tuple[float, float]=None):
        print("Jet power doesn't support plot range")

    

