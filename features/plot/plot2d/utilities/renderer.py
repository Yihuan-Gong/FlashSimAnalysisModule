from typing import Tuple
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm, SymLogNorm
import matplotlib.pyplot as plt
from astropy import units as u
import numpy as np

from ..models import Plot2dInfoModel
from .....models.interfaces import Data2dAxisReturnModel

class Renderer:
    
    def renderPlot(
        self, 
        timeMyr: float,
        value2d: u.Quantity,
        axis: Data2dAxisReturnModel, 
        plotInfo: Plot2dInfoModel,
    ) -> Tuple[Figure, plt.Axes]:
        if (plotInfo.fig == None or plotInfo.ax == None):
            plotInfo.fig, plotInfo.ax = plt.subplots()
        
        axisUnit = axis.horizontalAxis[1].unit.to_string()
        valueUnit = value2d.unit.to_string()
        
        # Render value2d to the image (image belongs to ax)
        image = plotInfo.ax.imshow(
            np.flipud(value2d.value.transpose()), 
            extent=[
                axis.horizontalAxis[1].value[0], axis.horizontalAxis[1].value[-1],
                axis.verticalAxis[1].value[0], axis.verticalAxis[1].value[-1],
            ],
            vmax=None if plotInfo.isLog else plotInfo.zlimMax,
            vmin=None if plotInfo.isLog else plotInfo.zlimMin,
            cmap=plotInfo.color,
            norm=SymLogNorm(
                linthresh=self.__adjustZlimThresh(plotInfo).zlimThresh, 
                vmin=plotInfo.zlimMin, vmax=plotInfo.zlimMax) \
                if plotInfo.isLog else None
        )

        # Add colorbar to ax
        cbar = plotInfo.fig.colorbar(image, ax=plotInfo.ax)
        cbar.set_label(f"{valueUnit}")

        # Time indication on the upper left
        if (plotInfo.showTimeInfo):
            imgaeXcoorPercent = -42
            imageYcoorPercent = 42
            plotInfo.ax.text(
                image.get_shape()[0]*imgaeXcoorPercent/100, 
                image.get_shape()[1]*imageYcoorPercent/100, 
                f"time = {timeMyr}Myr", 
                color='black', 
                fontsize=10
            )
        
        plotInfo.ax.set_title(f"{plotInfo.title}")
        plotInfo.ax.set_xlabel(f"{axis.horizontalAxis[0]} ({axisUnit})")
        plotInfo.ax.set_ylabel(f"{axis.verticalAxis[0]} ({axisUnit})")
        return plotInfo.fig, plotInfo.ax
    
    
    def __adjustZlimThresh(self, plotInfo: Plot2dInfoModel) -> Plot2dInfoModel:
        zlimThresh = plotInfo.zlimThresh
        if (zlimThresh == None):
            if (plotInfo.zlimMin == None):
                raise ValueError("You must set zlimThresh for zlimMin for log plot")
            else:
                plotInfo.zlimThresh = plotInfo.zlimMin
        return plotInfo