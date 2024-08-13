from dataclasses import dataclass
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

@dataclass
class Plot2dInfoModel:
    '''
        zlimThresh is needed for plotting logscale with negative data value
    '''
    title: str
    isLog: bool = False
    color: str = "viridis"
    zlimMin: float = None
    zlimMax: float = None
    zlimThresh: float = None
    showTimeInfo: bool = True
    fig: plt.Figure = None
    ax: plt.Axes = None