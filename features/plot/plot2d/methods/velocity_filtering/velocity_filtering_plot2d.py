from typing import Dict, Tuple
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .enums import VelocityFilteringField
from ...utilities import Renderer
from ...models import Plot2dInfoModel
from .....calculate_data.calculate_data2d import (
    Data2dAnalyzor,
    VelocityFilteringMode,
    VelocityFilteringCalculationInfoModel,
)
from ......models import SimFileModel

class VelocityFilteringPlot2d:
    __fieldToMode: Dict[VelocityFilteringField, VelocityFilteringMode]
    
    def __init__(self) -> None:
        self.__fieldToMode = {
            VelocityFilteringField.turbVtotal : VelocityFilteringMode.BulkTurb,
            VelocityFilteringField.scale : VelocityFilteringMode.BulkTurb,
            VelocityFilteringField.compVtotal : VelocityFilteringMode.CompSole,
            VelocityFilteringField.soleVtotal : VelocityFilteringMode.CompSole,
            VelocityFilteringField.turbCompVtotal : VelocityFilteringMode.TurbCompSole,
            VelocityFilteringField.turbSoleVtotal : VelocityFilteringMode.TurbCompSole
        } 
    
    
    def plotByField(
        self, 
        field: VelocityFilteringField,
        axis: str,
        simFile: SimFileModel, 
        calculationInfo: VelocityFilteringCalculationInfoModel,
        plotInfo: Plot2dInfoModel
    ) -> Tuple[Figure, plt.Axes]:
        result = Data2dAnalyzor().velocityFiltering(
            mode=self.__fieldToMode[field],
            axis=axis,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Renderer().renderPlot(
            value2d=getattr(result, f"{field}".split(".")[-1]),
            axis=result,
            plotInfo=plotInfo
        )
    
