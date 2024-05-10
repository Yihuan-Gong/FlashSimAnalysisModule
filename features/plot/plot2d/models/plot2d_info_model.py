from dataclasses import dataclass
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

@dataclass
class Plot2dInfoModel:
    figure: Figure = None
    ax: plt.Axes = None