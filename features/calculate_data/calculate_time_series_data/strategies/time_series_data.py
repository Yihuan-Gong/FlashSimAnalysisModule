from ..models.time_series_calculation_info_model import TimeSeriesCalculationInfoModel
from .....models.sim_file_model import SimFileModel
from .....models.data1d_return_model.data1d_return_model import Data1dReturnModel

class TimeSeriesData:
    _simFile: SimFileModel
    _calculationInfo: TimeSeriesCalculationInfoModel

    
    def setInputs(self, simFile: SimFileModel, calculationInfo: TimeSeriesCalculationInfoModel):
        self._simFile = simFile
        self._calculationInfo = calculationInfo

    
    def getData(self) -> Data1dReturnModel:
        raise NotImplementedError("Please use the sub-class, such as GasPropertyTimeSeriesData")