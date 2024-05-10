from typing import Tuple, List
import yt
import mirpyidl as idl
import numpy as np

from .velocity_filtering_strategy import VelocityFilteringStrategy
from ..model import CompSoleVelocityFilteringData3dReturnModel
from ....models.data3d_return_model import Data3dReturnModel
from .......services.yt_raw_data_helper import YtRawDataHelper

class CompSoleVelocityFilteringData3dStrategy\
    (VelocityFilteringStrategy):
    def getData(self) -> Data3dReturnModel:
        return super().getData()
