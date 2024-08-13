from dataclasses import dataclass
from typing import Tuple

from ......models.interfaces import (
    CoordinateModel, 
    DataNdCalculationInfoModel
)


@dataclass
class YtFieldCalculationInfoModel(
    DataNdCalculationInfoModel, 
    CoordinateModel
):
    fieldName: Tuple[str, str]
    