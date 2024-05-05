from typing import List

from ..utility import GasField
from ..data_base import PandasHelper
from ..utility import Shape


class Analyzor:
    _gasProperty: GasField = None
    _basePath: str = None
    _hdf5Title: str = None
    _fileStepMyr: int = 1
    _shape: Shape = Shape.Sphere
    _rhoIndex: float = None


    def setField(self, gasField: GasField):
        self._gasProperty = gasField
        return self

    
    def setBasePath(self, basePath: str):
        self._basePath = basePath
        return self
    
    
    def setHdf5Title(self, hdf5Title: str):
        self._hdf5Title = hdf5Title
        return self
    

    def setFileStepMyr(self, fileStepMyr: int):
        self._fileStepMyr = fileStepMyr
        return self
    

    def setShape(self, shape: Shape):
        self._shape = shape
        return self
    

    def setRhoIndex(self, rhoIndex: float):
        self._rhoIndex = rhoIndex
        return self
    

    def resetDataBase(self):
        if (self._basePath is None):
            raise Exception("You should excute .setBasePath() beforehand")
        if (self._gasProperty is None):
            raise Exception("You should excute .setField() beforehand")
        PandasHelper().resetDataBase(self._basePath, self._gasProperty, self._shape)
        return self


    def _checkBasicSetting(self):
        if (self._gasProperty is None):
            raise Exception("Please excute .setField()")
        if (self._basePath is None):
            raise Exception("Please excute .setBasePath()")
        if (self._hdf5Title is None):
            raise Exception("Please excute .setHdf5Title()")
        