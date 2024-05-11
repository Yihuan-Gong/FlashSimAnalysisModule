from dataclasses import dataclass
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

@dataclass
class Plot2dInfoModel:
    title: str
    isLog: bool = False
    color: str = "viridis"
    zlimMin: float = None
    zlimMax: float = None
    fig: plt.Figure = None
    ax: plt.Axes = None