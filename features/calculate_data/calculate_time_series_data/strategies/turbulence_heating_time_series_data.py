from typing import List

from .time_series_data import TimeSeriesData
from ..models.turbulence_heating_time_series_calculation_info_model import TurbulenceHeatingTimeSeriesCalculationInfoModel
from .....data_base.db_model import DbModel
from .....data_base.turb_db_model import TurbDbModel
from .....data_base.turb_pandas_helper import TurbPandasHelper
from .....enum.shape import Shape
from .....models.data1d_return_model.data1d_return_model import Data1dReturnModel
from .....models.data1d_return_model.turb_data_return_model import TurbDataReturnModel
from .....services.yt_ds_helper import YtDsHelper
from .....utility.turbulence_analyzor import TurbulenceAnalyzor


class TurbulenceHeatingTimeSeriesData(TimeSeriesData):
    t: range
    fileNums: List[int]
    rhoIndex: float

    def __init__(self) -> None:
        super().__init__()
    

    def getData(self) -> Data1dReturnModel:
        '''
            Return: Data1dReturnModel(
                x: List[float],                     # time in Myr
                value: List[TurbDataReturnModel],   
                valueUnit: str                      # "erg/s"
                label: Tuple[float, str]            # (r, unit of r)
            )
        '''
        calculationInfo: TurbulenceHeatingTimeSeriesCalculationInfoModel\
            = self._calculationInfo
        self.rhoIndex = calculationInfo.rhoIndex
        self.t = range(
            calculationInfo.tStartMyr,
            calculationInfo.tEndMyr,
            calculationInfo.tStepMyr
        )
        self.fileNums = [int(x/self._simFile.fileStepMyr) for x in self.t]
        
        if (self._calculationInfo.shape != Shape.Box):
            raise ValueError("Turbulence heating only support box shape!")
        if (self.rhoIndex is None):
            raise ValueError("You must set the rho index")
        return Data1dReturnModel(
            x=self.t,
            value=self.__getHeatingRateTs(),
            valueUint="erg/s",
            label=(self._calculationInfo.rKpc, "kpc")
        )
    
    
    def __getHeatingRateTs(self) -> TurbDataReturnModel:
        turbDataList: List[TurbDbModel] = []
        for timeMyr in self.t:
            turbData = TurbPandasHelper().getTurbDataFromCsv(
                simBasePath=self._simFile.simPath,
                shape=self._calculationInfo.shape,
                rKpc=self._calculationInfo.rKpc,
                tMyr=timeMyr,
                rhoIndex=self.rhoIndex
            )
            if (turbData is not None):
                turbDataList.append(turbData)
                continue

            ds = YtDsHelper().loadDs(self._simFile, timeMyr)
            # yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, int(timeMyr/self.fileStepMyr)))
            turbDataTemp = TurbulenceAnalyzor()\
                .setDensityWeightingIndex(self.rhoIndex) \
                .setDataSeries(ds) \
                .setBoxSize(self._calculationInfo.rKpc) \
                .calculatePowerSpectrum() \
                .getDissipationRate()
            turbData = TurbDbModel(
                rhoIndex=self.rhoIndex,
                upperLimit=turbDataTemp["turb_heating_rate_upper_limit"],
                lowerLimit=turbDataTemp["turb_heating_rate_lower_limit"]
            )
            turbDataList.append(turbData)
            TurbPandasHelper().writeDataIntoCsv(
                simBasePath=self._simFile.simPath, 
                field="TurbulenceHeating", 
                shape=self._calculationInfo.shape,
                dbModelList=[DbModel(
                    rKpc=self._calculationInfo.rKpc, 
                    tMyr=timeMyr, 
                    value=turbData
                )]
            )

        return TurbDataReturnModel(
            rhoIndex=self.rhoIndex,
            upperLimit=[x.upperLimit for x in turbDataList],
            lowerLimit=[x.lowerLimit for x in turbDataList]
        )
        
