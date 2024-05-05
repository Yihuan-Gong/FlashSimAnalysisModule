from .strategies import *
from .enums.time_series_mode import TimeSeriesMode
from .models.time_series_calculation_info_model import TimeSeriesCalculationInfoModel
from ....models.data1d_return_model.data1d_return_model import Data1dReturnModel
from ....models.sim_file_model import SimFileModel

class TimeSeriesAnalyzor:
    __timeSeriesStragy: TimeSeriesData
    

    def setInputs(self, timeSeriesMode: TimeSeriesMode, simFile: SimFileModel, 
                  calculationInfo: TimeSeriesCalculationInfoModel):
        className = f"{timeSeriesMode}".split(".")[-1] + TimeSeriesData.__name__
        self.__timeSeriesStragy = globals()[className]()
        self.__timeSeriesStragy.setInputs(simFile, calculationInfo)
        return self


    def getData(self) -> Data1dReturnModel:
        return self.__timeSeriesStragy.getData()
    
    