from ..models.input_models.data2d_calculation_info_model import Data2dCalculationInfoModel
from ..models.return_models.data2d_return_model import Data2dReturnModel
from .....models.sim_file_model import SimFileModel

class Data2D:
    _simFile: SimFileModel
    _calculationInfo: Data2dCalculationInfoModel

    def setInputs(self, simFile: SimFileModel, calculationInfo: Data2dCalculationInfoModel):
        self._simFile = simFile
        self._calculationInfo = calculationInfo
        return self
    
    
    def getData(self) -> Data2dReturnModel:
        pass