import matplotlib.pyplot as plt
import yt
import numpy as np
import pandas as pd
from typing import Tuple

from python.modules.data.data import DataModel

from .time_series_data import TimeSeriesData
from ...utility import GasField, FieldAdder
from ...data_base import PandasHelper, DataBaseModel


class GasPropertyTimeSeriesData(TimeSeriesData):
    def __init__(self, gasProperty: GasField) -> None:
        super().__init__()
        self.gasProperty = gasProperty
        self.gasFieldName = self.__getFieldName()
        self.weightFieldName = ("gas", "mass")
        FieldAdder.AddFields()
    

    def getData(self) -> DataModel:
        return DataModel(
            x=self.t,
            value=self.__getTimeSeries(),
            label=(self.rKpc, "kpc")
        )
    

    def __getTimeSeries(self):
        timeSeries = []
        for timeMyr in self.t:
            # Find the calculated result from data base
            value = self.pandasHelper.getDataFromCsv(self.basePath, self.gasProperty, self.rKpc, timeMyr)
            if (value is not None):
                timeSeries.append(value)
                continue
            
            # If the calculated result does not exist in data base,
            # we calculate one here
            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr/self.fileStepMyr))
            if (self.gasProperty == GasField.Luminosity):
                ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr/self.fileStepMyr),
                             default_species_fields="ionized")
                yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
                sp = ds.sphere((0,0,0), (self.rKpc, "kpc"))
                value = float(sp.quantities.total_quantity(self.gasFieldName).d)
            else:
                ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, timeMyr/self.fileStepMyr))
                sp = ds.sphere((0,0,0), (self.rKpc, "kpc"))
                value = float(sp.quantities.weighted_average_quantity(self.gasFieldName, self.weightFieldName).d)
            del ds
            del sp

            # Write the calculated result into data base
            timeSeries.append(value)
            self.pandasHelper.writeDataIntoCsv(self.basePath, self.gasProperty, [DataBaseModel(self.rKpc, timeMyr, value)])

        return timeSeries
    
    
    def __getFieldName(self):
        if (self.gasProperty == GasField.Density):
            return ('gas', 'density')
        elif (self.gasProperty == GasField.Temperature):
            return ('gas', 'temp_in_keV')
        elif (self.gasProperty == GasField.Pressure):
            return ('gas', 'pressure')
        elif (self.gasProperty == GasField.Entropy):
            return ('gas', 'entropy')
        elif (self.gasProperty == GasField.Luminosity):
            return ("gas","xray_luminosity_0.5_7.0_keV")
        
    
    # def __init__(self, basePath: str, gasProperty: GasField, 
    #              startTimeMyr: float, endTimeMyr: float, stepMyr: float,
    #              myrPerFile: bool = True) -> None:
    #     super().__init__(basePath, startTimeMyr, endTimeMyr, stepMyr, myrPerFile)
    #     FieldAdder.AddFields()
    #     self.gasProperty = gasProperty
    #     self.field = self.__getFieldName()
    #     self.weight = ("gas", "mass")
    #     self.pandasHelper = PandasHelper()


    # def plot(self, ax: plt.Axes, rKpc: float, ylim: Tuple[float, float]=None) -> plt.Axes:
    #     timeSeries = self.__getTimeSeries(rKpc)
    #     self.__initAxes(ax, ylim=ylim)
    #     ax.plot(self.timesMyr, timeSeries, label="%d kpc"%rKpc)
    #     ax.legend()
    #     return ax

    
    # def plotRange(self, ax: plt.Axes, rStartKpc: float, rEndKpc: float, rStepKpc: float,  
    #               ylim: Tuple[float, float]=None) -> plt.Axes:
    #     for rKpc in range(rStartKpc, rEndKpc, rStepKpc):
    #         timeSeries = self.__getTimeSeries(rKpc)
    #         ax.plot(self.timesMyr, timeSeries, label="%d kpc"%rKpc)
    #     ax.set(xlabel='r $(kpc)$')
    #     ax.legend()
    #     return ax


    # def __initAxes(self, ax: plt.Axes, ylim: Tuple[float, float]=None):
    #     ax.set(xlabel='r $(kpc)$')
        
    #     if (self.gasProperty == GasField.Temperature):
    #         ax.set(ylabel='<kT> $(keV)$')
    #     elif (self.gasProperty == GasField.Density):
    #         ax.set(ylabel='<Density> $(g/cm^3)$')
    #     elif (self.gasProperty == GasField.Pressure):
    #         ax.set(ylabel='<Pressure> $(Ba)$')
    #     elif (self.gasProperty == GasField.Entropy):
    #         ax.set(ylabel='<S> $(keV cm^2)$')
    #     elif (self.gasProperty == GasField.Luminosity):
    #         ax.set(ylabel='Total Luminosity $(erg/s)$')

    #     if (ylim is not None):
    #         ax.set(ylim=ylim)

    





    


