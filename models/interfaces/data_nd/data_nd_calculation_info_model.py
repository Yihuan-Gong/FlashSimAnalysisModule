from dataclasses import dataclass
from typing import Protocol
from typing_extensions import runtime_checkable

@dataclass
@runtime_checkable
class DataNdCalculationInfoModel(Protocol):
    timeMyr: float
    rBoxKpc: float