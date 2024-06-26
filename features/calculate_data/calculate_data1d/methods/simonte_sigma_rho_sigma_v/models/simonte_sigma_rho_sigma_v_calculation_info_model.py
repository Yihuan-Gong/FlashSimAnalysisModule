from dataclasses import dataclass
from typing import Tuple

from .....calculate_data3d import VelocityFilteringField
from .......models.interfaces.coordinate_model import CoordinateModel
from .......models.interfaces.data_nd.data_nd_calculation_info_model import DataNdCalculationInfoModel
from .......models.interfaces.velocity_field_model import VelocityFieldModel



@dataclass
class SimonteSigmaRhoSigmaVCalculationInfoModel(
    DataNdCalculationInfoModel, 
    CoordinateModel, 
    VelocityFieldModel
):
    '''
        densityFilteringMode: "radial" or "box"
        filteringBoxSizeKpc: mode "box" only
    '''
    velocityField: VelocityFilteringField
    bulkTurbFilteringMinScale: int = 4
    bulkTurbFilteringMaxScale: int = None
    bulkTurbFilteringEps: float = 0.1
    densityFieldName: Tuple[str, str] = ("gas", "density")
    densityFilteringMode: str = "radial"
    filteringBoxSizeKpc: float = None
    numberOfCubeEachSide: int = 6
    soundSpeedFieldName: Tuple[str, str] = ("gas", "sound_speed")
    