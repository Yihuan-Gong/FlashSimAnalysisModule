from dataclasses import dataclass

from ..Enum.GasField import GasField
from ..Enum.SeriesType import SeriesType

@dataclass
class DataModel:
    rKpc : float
    tMyr : float
    value : float