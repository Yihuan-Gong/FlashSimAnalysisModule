from dataclasses import dataclass
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

@dataclass
class Plot1dInfoModel:
    title: str = None
    xLabel: str = "default"
    yLabel: str = "default"
    lineLabel: str = "default"
    lineColor: str = "default"
    lineStyle: str = "default"
    lineAlpha: float = 1
    showLegend: bool = True
    xLogScale: bool = False
    yLogScale: bool = False
    xLowerBound: float = None
    xUpperBound: float = None
    yLowerBound: float = None
    yUpperBound: float = None
    fig: plt.Figure = None
    ax: plt.Axes = None