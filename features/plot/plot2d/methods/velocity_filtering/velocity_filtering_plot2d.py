from typing import Dict, Tuple
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


from ...utilities import Renderer
from ...models import Plot2dInfoModel
from .....calculate_data.calculate_data2d import (
    Data2dAnalyzor,
    VelocityFilteringMode,
    VelocityFilteringField,
    VelocityFilteringCalculationInfoModel,
)
from ......models import SimFileModel

class VelocityFilteringPlot2d:
    
    def plotByField(
        self, 
        field: VelocityFilteringField,
        axis: str,
        simFile: SimFileModel, 
        calculationInfo: VelocityFilteringCalculationInfoModel,
        plotInfo: Plot2dInfoModel
    ) -> Tuple[Figure, plt.Axes]:
        result = Data2dAnalyzor().velocityFilteringByField(
            field=field,
            axis=axis,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Renderer().renderPlot(
            timeMyr=calculationInfo.timeMyr,
            value2d=getattr(result, f"{field}".split(".")[-1]),
            axis=result,
            plotInfo=plotInfo
        )
    
