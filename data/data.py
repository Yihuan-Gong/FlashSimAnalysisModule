from abc import ABC, abstractmethod
from typing import List

from .data_model import DataModel
from ..data_base import PandasHelper

class Data(ABC):
    basePath: str
    fileStepMyr: int = 1
    pandasHelper: PandasHelper

    def __init__(self) -> None:
        self.pandasHelper = PandasHelper()


    def setBasePath(self, basePath: str):
        self.basePath = basePath
        return self


    def setFileStepMyr(self, fileStepMyr: int):
        self.fileStepMyr = fileStepMyr
        return self


    @abstractmethod
    def getData(self) -> DataModel:
        pass
