from .data2d_input_model import Data2dInputModel
from ..utility.hdf5_mode import Hdf5Mode

class Data2D:
    _data2dInputModel: Data2dInputModel

    def __init__(self) -> None:
        self._data2dInputModel = None

    def setFileProperties(self, data2dInputModel: Data2dInputModel):
        self._data2dInputModel = data2dInputModel
        return self