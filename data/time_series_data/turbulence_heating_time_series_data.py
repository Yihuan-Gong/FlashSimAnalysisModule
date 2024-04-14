import yt
from typing import List


from ..time_series_data.time_series_data import TimeSeriesData
from ..data_model import DataModel
from ..turb_data_model import TurbDataModel
from ...analyzor.turbulence_analyzor import TurbulenceAnalyzor
from ...data_base import DbModel, TurbPandasHelper, TurbDbModel
from ...utility import GasField, Shape


class TurbulenceHeatingTimeSeriesData(TimeSeriesData):
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
            x=self.t,
            value=self.__getHeatingRateTs(),
            label=(self.rKpc, "kpc")
        )
    

    def __getHeatingRateTs(self) -> TurbDataModel:
        turbDataList: List[TurbDbModel] = []
        for timeMyr in self.t:
            turbData = self.turbPandasHelper.getTurbDataFromCsv(
                self.basePath,
                self.shape,
                self.rKpc,
                timeMyr,
                self.rhoIndex
            )
            if (turbData is not None):
                turbDataList.append(turbData)
                continue

            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, int(timeMyr/self.fileStepMyr)))
            turbDataTemp = self.turbulenceAnalyzor.setDensityWeightingIndex(self.rhoIndex) \
                                           .setDataSeries(ds) \
                                           .setBoxSize(self.rKpc) \
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
                [DbModel(rKpc=self.rKpc, tMyr=timeMyr, value=turbData)]
            )

        return TurbDataModel(
            rhoIndex=self.rhoIndex,
            upperLimit=[x.upperLimit for x in turbDataList],
            lowerLimit=[x.lowerLimit for x in turbDataList]
        )



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