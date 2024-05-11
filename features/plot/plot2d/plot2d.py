from typing import Tuple
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .models import Plot2dInfoModel
from .methods.velocity_filtering import (
    VelocityFilteringField,
    VelocityFilteringPlot2d
)
from .utilities import Renderer
from ...calculate_data.calculate_data2d import *

class Plot2d:
    
    def velocityFiltering(
        self, 
        field: VelocityFilteringField,
        axis: str,
        simFile: SimFileModel, 
        calculationInfo: VelocityFilteringCalculationInfoModel,
        plotInfo: Plot2dInfoModel
    ) -> Tuple[Figure, plt.Axes]:
        return VelocityFilteringPlot2d().plotByField(
            field=field,
            axis=axis,
            simFile=simFile,
            calculationInfo=calculationInfo,
            plotInfo=plotInfo
        )
    
    
    def losVelDispersion(
        self,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: LosDispersionCalculationInfoModel,
        plotInfo: Plot2dInfoModel
    ) -> Tuple[Figure, plt.Axes]:
        result = Data2dAnalyzor().losVelDispersion(
            axis=axis,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Renderer().renderPlot(
            value2d=result.value,
            axis=result,
            plotInfo=plotInfo
        )
    
    
    def turbulenceHeatingVazza(
        self,
        mode: TurbulenceHeatingVazzaMode,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel,
        plotInfo: Plot2dInfoModel
    ) -> Tuple[Figure, plt.Axes]:
        result = Data2dAnalyzor().turbulenceHeatingVazza(
            mode=mode,
            axis=axis,
            simFile=simFile,
            calculationInfo=calculationInfo
        )
        return Renderer().renderPlot(
            value2d=result.heatingPerVolume.to("erg/(s*kpc**3)"),
            axis=result,
            plotInfo=plotInfo
        )
        
    
    
    
    

        