from typing import List, Tuple
import yt

from .plot2d_info_model import Plot2dInfoModel
from ..enums.yt_ploter2d_mode import YtPloter2DMode
from dataclasses import dataclass

@dataclass
class YtPlot2dInfoModel(Plot2dInfoModel):
    plotMode: YtPloter2DMode
    field: Tuple[str, str]
    center: yt.YTArray = yt.YTArray([0,0,0], "kpc")
    markPointPos: List[any] = [(0,0)]
    zlimMin: float = None
    zlimMax: float = None
    contour: str = None
    contourNum: int = 20
    markGrid: bool = False
    markParticles: bool = False
    markVelocity = False
    velocityScale: float = 1e10