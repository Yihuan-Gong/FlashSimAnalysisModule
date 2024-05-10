from typing import Tuple
from astropy import units as u
from dataclasses import dataclass
import numpy as np

@dataclass
class Data2dReturnModel:
    horizontalAxis: u.Quantity
    verticalAxis: u.Quantity