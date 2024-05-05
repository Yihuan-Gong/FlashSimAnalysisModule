from typing import Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class Data2dReturnModel:
    value: np.ndarray
    horizontalAxis: Tuple[str, np.ndarray]
    verticalAxis: Tuple[str, np.ndarray]