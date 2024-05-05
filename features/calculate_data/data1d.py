from abc import ABC, abstractmethod
from typing import List

from .data_model import DataModel
from ..data_base import PandasHelper
from ..utility import Shape, YtDsHelper

class Data(ABC):
    basePath: str
    hdf5FileTitle: str
    fileStepMyr: int = 1
    pandasHelper: PandasHelper
    ytDsHelper: YtDsHelper
    shape: Shape
    


    def __init__(self) -> None:
        self.pandasHelper = PandasHelper()
        self.ytDsHelper = YtDsHelper()
        self.hdf5FileTitle = "perseus_merger"


    def setBasePath(self, basePath: str):
        self.basePath = basePath
        return self


    def setFileStepMyr(self, fileStepMyr: int):
        self.fileStepMyr = fileStepMyr
        return self
    
    def setShape(self, shape: Shape):
        self.shape = shape
    

    def setHdf5FileTitle(self, fileTitle: str):
        self.hdf5FileTitle = fileTitle


    @abstractmethod
    def getData(self) -> DataModel:
        pass
