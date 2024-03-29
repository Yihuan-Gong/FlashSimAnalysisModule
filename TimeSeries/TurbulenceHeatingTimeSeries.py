import matplotlib.pyplot as plt
import yt
import numpy as np
import pandas as pd
import os
from typing import Tuple
from python.modules.TimeSeries.TimeSeries import TimeSeries
from python.modules.FieldAdder import FieldAdder
from python.modules.TurbulenceAnalyzor import TurbulenceAnalyzor

class TurbulenceHeatingTimeSeries(TimeSeries):
    def __init__(self, basePath: np.str, startTimeMyr: np.float, endTimeMyr: np.float, stepMyr: np.float, myrPerFile: np.bool = True) -> None:
        super().__init__(basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile)
        self.turbulenceAnalyzor = TurbulenceAnalyzor()


    def plot(self, ax: plt.Axes, rKpc: float, ylim: Tuple[float, float]=None) -> plt.Axes:
        heatingRates = []
        for timeMyr in self.timesMyr:
            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr))
            self.turbulenceAnalyzor.setDensityWeightingIndex(1).setDataSeries(ds).setBoxSize(rKpc)
            data = self.turbulenceAnalyzor.calculatePowerSpectrum().getDissipationRate()
            heatingRates.append(data['turb_heating_rate'])
        ax.plot(self.timesMyr, heatingRates, label="%d kpc turbulence heating rate"%rKpc)
        ax.set_xlabel("t (Myr)")
        ax.set_ylabel("Power (erg/s)")
        ax.legend()


    def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
                  ylim: Tuple[float, float]=None) -> plt.Axes:
        for rKpc in range(rStartKpc, rEndKpc + 1, rStepKpc):
            self.plot(ax, rKpc, ylim)