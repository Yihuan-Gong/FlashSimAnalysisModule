import matplotlib.pyplot as plt
import yt
import numpy as np
import pandas as pd
import os
from typing import Tuple
from python.modules.TimeSeries.TimeSeries import TimeSeries
from python.modules.GasProperty import GasProperty
from python.modules.FieldAdder import FieldAdder


class GasPropertyTimeSeries(TimeSeries):
    def __init__(self, basePath: str, gasProperty: GasProperty, 
                 startTimeMyr: float, endTimeMyr: float, stepMyr: float,
                 myrPerFile: bool = True) -> None:
        super().__init__(basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile)
        FieldAdder.AddFields()
        self.gasProperty = gasProperty
        self.field = self.__getFieldName()
        self.weight = ("gas", "mass")
        # self.data = self.__getDataFromCsv()


    def plot(self, ax: plt.Axes, rKpc: float, ylim: Tuple[float, float]=None) -> plt.Axes:
        timeSeries = self.__getTimeSeries(rKpc)
        self.__initAxes(ax, ylim=ylim)
        ax.plot(self.timesMyr, timeSeries, label="%d kpc"%rKpc)
        ax.legend()
        return ax

    
    def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
                  ylim: Tuple[float, float]=None) -> plt.Axes:
        for rKpc in range(rStartKpc, rEndKpc, rStepKpc):
            timeSeries = self.__getTimeSeries(rKpc)
            ax.plot(self.timesMyr, timeSeries, label="%d kpc"%rKpc)
        ax.set(xlabel='r $(kpc)$')
        ax.legend()
        return ax


    def __getTimeSeries(self, rKpc: float):
        timeSeries = []
        for timeMyr in self.timesMyr:
            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr))
            if (self.gasProperty == GasProperty.Luminosity):
                ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr),
                             default_species_fields="ionized")
                yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
                sp = ds.sphere((0,0,0), (rKpc, "kpc"))
                timeSeries.append(sp.quantities.total_quantity(self.field))
            else:
                ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr))
                sp = ds.sphere((0,0,0), (rKpc, "kpc"))
                timeSeries.append(sp.quantities.weighted_average_quantity(self.field, self.weight))
            del ds
            del sp

        return timeSeries
        
    

    def __initAxes(self, ax: plt.Axes, ylim: Tuple[float, float]=None):
        ax.set(xlabel='r $(kpc)$')
        
        if (self.gasProperty == GasProperty.Temperature):
            ax.set(ylabel='<kT> $(keV)$')
        elif (self.gasProperty == GasProperty.Density):
            ax.set(ylabel='<Density> $(g/cm^3)$')
        elif (self.gasProperty == GasProperty.Pressure):
            ax.set(ylabel='<Pressure> $(Ba)$')
        elif (self.gasProperty == GasProperty.Entropy):
            ax.set(ylabel='<S> $(keV cm^2)$')
        elif (self.gasProperty == GasProperty.Luminosity):
            ax.set(ylabel='Total Luminosity $(erg/s)$')

        if (ylim is not None):
            ax.set(ylim=ylim)

    

    def __getFieldName(self):
        if (self.gasProperty == GasProperty.Density):
            return ('gas', 'density')
        elif (self.gasProperty == GasProperty.Temperature):
            return ('gas', 'temp_in_keV')
        elif (self.gasProperty == GasProperty.Pressure):
            return ('gas', 'pressure')
        elif (self.gasProperty == GasProperty.Entropy):
            return ('gas', 'entropy')
        elif (self.gasProperty == GasProperty.Luminosity):
            return ("gas","xray_luminosity_0.5_7.0_keV")
        
    
    # def __getDataCsvPath(self):
    #     return "./Asset/%s/%s_ts.csv"%(self.basePath, self.__getFieldName()[1])
    
    
    # def __getDataFromCsv(self):
    #     path = self.__getDataCsvPath()
    #     if os.path.exists(path):
    #         data = pd.read_csv(path)
    #         data.sort_values(by="time")
    #         return data
    #     else:
    #         return pd.DataFrame()



    


