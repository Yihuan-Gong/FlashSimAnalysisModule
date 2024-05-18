from typing import List, TypeVar
from dataclasses import dataclass
import copy

from .....models.interfaces import DataNdCalculationInfoModel

T = TypeVar("T")


@dataclass
class Video2dInfoModel:
    tStartMyr: float
    tEndMyr: float
    tStepMyr: float
    fps: int = 20
    videoDir: str = "default"
    videoName: str = "default"
    imageDir: str = "default"
    
    
    def getCalcInfoList(
        self, 
        calculationInfo: T
    ) -> List[T]:
        
        if (not isinstance(calculationInfo, DataNdCalculationInfoModel)):
            raise ValueError("calculationInfo should be the instance of DataNdCalculationInfoModel")
        
        result: List[T] = []
        for timeMyr in range(self.tStartMyr, self.tEndMyr, self.tStepMyr):
            newCaluInfo = copy.deepcopy(calculationInfo)
            newCaluInfo.timeMyr = timeMyr
            result.append(newCaluInfo)
        return result
            