from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class ProfileCalculationInfoModel:
    rStartKpc: float
    rEndKpc: float
    rStepKpc: float
    tMyr: float
    
    def getRList(self):
        return np.arange(
            self.rStartKpc,
            self.rEndKpc,
            self.rStepKpc
        )

