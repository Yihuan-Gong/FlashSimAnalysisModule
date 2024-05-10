from typing import Tuple
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from ..models.plot2d_info_model import Plot2dInfoModel
from ....calculate_data.calculate_data2d import Data2dCalculationInfoModel
from .....models import SimFileModel

class Ploter2D:
    _simFile: SimFileModel
    _calculationModel: Data2dCalculationInfoModel
    _plotModel: Plot2dInfoModel
    
    
    def setInputs(self, simFile: SimFileModel, calculationModel: Data2dCalculationInfoModel,
                  plotModel: Plot2dInfoModel):
        self._simFile = simFile
        self._calculationModel = calculationModel
        self._plotModel = plotModel
        return self
        
    
    def getPlot(self) -> Tuple[Figure, plt.Axes]:
        raise NotImplementedError("Please use the subclass")