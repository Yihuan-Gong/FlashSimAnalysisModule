import matplotlib.pyplot as plt
import yt
import numpy as np
import pandas as pd
import os
from typing import List

from python.modules.data.data import DataModel

from ..time_series_data.time_series_data import TimeSeriesData
from ...analyzor.turbulence_analyzor import TurbulenceAnalyzor
from ...data_base import PandasHelper, DataBaseModel
from ...utility import GasField


class TurbulenceHeatingTimeSeriesData(TimeSeriesData):
    def __init__(self) -> None:
        super().__init__()
        self.turbulenceAnalyzor = TurbulenceAnalyzor()
    

    def getData(self) -> DataModel:
        return DataModel(
            x=self.t,
            value=self.__getHeatingRateTs(),
            label=(self.rKpc, "kpc")
        )
    

    def __getHeatingRateTs(self) -> List[float]:
        heatingRates = []
        for timeMyr in self.t:
            value = self.pandasHelper.getDataFromCsv(self.basePath, GasField.TurbulenceHeating, self.rKpc, timeMyr)
            if (value is not None):
                heatingRates.append(value)
                continue
            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, int(timeMyr/self.fileStepMyr)))
            value = self.turbulenceAnalyzor.setDensityWeightingIndex(1) \
                                           .setDataSeries(ds) \
                                           .setBoxSize(self.rKpc) \
                                           .calculatePowerSpectrum() \
                                           .getDissipationRate()['turb_heating_rate']
            heatingRates.append(value)
            self.pandasHelper.writeDataIntoCsv(self.basePath, GasField.TurbulenceHeating, [DataBaseModel(self.rKpc, timeMyr, value)])
        return heatingRates



    # def __init__(self, basePath: np.str, startTimeMyr: np.float, endTimeMyr: np.float, stepMyr: np.float, myrPerFile: np.bool = True) -> None:
    #     super().__init__(basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile)
    #     self.turbulenceAnalyzor = TurbulenceAnalyzor()
    #     self.pandasHelper = PandasHelper()


    # def plot(self, ax: plt.Axes, rKpc: float, ylim: Tuple[float, float]=None) -> plt.Axes:
    #     heatingRates = []
    #     for timeMyr in self.timesMyr:
    #         value = self.pandasHelper.getDataFromCsv(self.basePath, GasField.TurbulenceHeating, rKpc, timeMyr)
    #         if (value is not None):
    #             heatingRates.append(value)
    #             continue
            
    #         ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr))
    #         self.turbulenceAnalyzor.setDensityWeightingIndex(1).setDataSeries(ds).setBoxSize(rKpc)
    #         value = self.turbulenceAnalyzor.calculatePowerSpectrum().getDissipationRate()['turb_heating_rate']
    #         heatingRates.append(value)
    #         self.pandasHelper.writeDataIntoCsv(self.basePath, GasField.TurbulenceHeating, [DataModel(rKpc, timeMyr, value)])

    #     ax.plot(self.timesMyr, heatingRates, label="%d kpc turbulence heating rate"%rKpc)
    #     ax.set_xlabel("t (Myr)")
    #     ax.set_ylabel("Power (erg/s)")
    #     ax.legend()


    # def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
    #               ylim: Tuple[float, float]=None) -> plt.Axes:
    #     for rKpc in range(rStartKpc, rEndKpc + 1, rStepKpc):
    #         self.plot(ax, rKpc, ylim)