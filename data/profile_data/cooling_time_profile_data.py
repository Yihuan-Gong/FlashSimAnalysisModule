import matplotlib.pyplot as plt
import yt
import numpy as np
from typing import Tuple

from .profile_data import ProfileData
from ..data import DataModel
from ...utility import FieldAdder, Constants


class CoolingTimeProfileData(ProfileData):
    def __init__(self):
        super().__init__()
        FieldAdder.AddFields()
        self.gasFieldName = ("gas", "cooling_time")
        

    def getData(self) -> DataModel:
        profile = self.__getProfile()
        return DataModel(
            x = np.array(profile.x).tolist(),
            value = np.array(profile[self.gasFieldName]).tolist(),
            label = (self.tMyr/1000, "Gyr")
        )

    
    def __coolingTime(self, field, data):
        internalEnergyPerVolume = (3/2) * 1.836 * data[('gas', 'electron_density')] * data[("gas", "temp_in_keV")]
        xrayEmissivity = data[('gas', 'xray_emissivity_0.5_7_keV')]
        return internalEnergyPerVolume/xrayEmissivity
    

    def __getProfile(self) -> yt.Profile1D:
        ds = yt.load(
                '%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, self.fileNum),
                default_species_fields="ionized"
            )
        yt.add_xray_emissivity_field(ds, 0.5, 7, table_type='apec', metallicity=0.3)
        ds.add_field(
            ("gas", "cooling_time"),
            function = self.__coolingTime,
            sampling_type='cell',
            units='Gyr',
            force_override=True
        )
        sp = ds.sphere('c', (self.rEndKpc, 'kpc'))
        numberOfDatas = int((self.rEndKpc - self.rStartKpc)/self.rStepKpc)
        profile = yt.Profile1D(
            sp, ('gas', 'radius'), numberOfDatas, self.rStartKpc, self.rEndKpc, False, weight_field=('gas', 'density')
        )
        profile.add_fields(self.gasFieldName)
        del ds
        del sp
        return profile
    

    # def __getProfile(self) -> yt.Profile1D:
    #     ds = yt.load(
    #             '%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, self.fileNum),
    #             default_species_fields="ionized"
    #         )
    #     yt.add_xray_emissivity_field(ds, 0.5, 7, table_type='apec', metallicity=0.3)
    #     ds.add_field(
    #         ("gas", "cooling_time"),
    #         function = self.__coolingTime,
    #         sampling_type='cell',
    #         units='Gyr',
    #         force_override=True
    #     )
    #     ad = ds.all_data()
    #     profile = yt.create_profile(
    #         ad,
    #         ("index", "radius"),
    #         self.gasFieldName,
    #         weight_field=("gas", "mass"),
    #         n_bins=(128, 128),
    #     )
    #     return profile
    
    

    # def plot(self, ax: plt.Axes, timeMyr: float, ylim: Tuple[float, float]=None):
    #     profile = self.__getProfile(timeMyr)
    #     label =  "%.1f Gyr"%(timeMyr/1000) if (self.myrPerFile) else "%.1f Gyr"%(timeMyr/100)
    #     self.__initPlot(ax, ylim)
    #     ax.plot(np.array(profile.x)/Constants.kpc, np.array(profile[self.gasField]), label=label)


    # def plotRange(self, ax: plt.Axes,  startTimeMyr: float, endTimeMyr: float, stepMyr: float,  
    #               ylim: Tuple[float, float]=None):
    #     self.__initPlot(ax, ylim)
    #     for timeMyr in range(startTimeMyr, endTimeMyr, stepMyr):
    #         profile = self.__getProfile(timeMyr)
    #         label =  "%.1f Gyr"%(timeMyr/1000) if (self.myrPerFile) else "%.1f Gyr"%(timeMyr/100)
    #         ax.plot(np.array(profile.x)/Constants.kpc, np.array(profile[self.gasField]), label=label)
    #     ax.legend()

    
    # def __initPlot(self, ax: plt.Axes, ylim: Tuple[float, float]=None):
    #     ax.set(
    #         xlabel='r $(kpc)$',
    #         ylabel="Cooling Time (Gyr)",
    #         xscale="log",
    #         yscale="log",
    #         xlim=(20, 2000),
    #         ylim=(0.3, 200),
    #     )


    
    

    
