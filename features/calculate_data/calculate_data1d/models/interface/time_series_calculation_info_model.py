from dataclasses import dataclass
from typing import List


@dataclass
class TimeSeriesCalculationInfoModel:
    tStartMyr: float
    tEndMyr: float
    tStepMyr: float
    rKpc: float
    
    def getTimeList(self) -> List[float]:
        return list(range(
            self.tStartMyr,
            self.tEndMyr,
            self.tStepMyr
        ))

    