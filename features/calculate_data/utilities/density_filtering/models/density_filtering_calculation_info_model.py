from dataclasses import dataclass
from typing import Tuple

from ......models.interfaces import (
    CoordinateModel, 
    DataNdCalculationInfoModel
)

@dataclass(kw_only=True)
class DensityFilteringCalculationInfoModel(
    DataNdCalculationInfoModel, 
    CoordinateModel
):
    '''
    densityFilteringMode: "radial" or "box"
    filteringBoxSizeKpc: mode "box" only
    '''
    densityFieldName: Tuple[str, str] = ("gas", "density")
    # densityFilteringMode: str = "radial"
    filteringBoxSizeKpc: float = None
    pass
