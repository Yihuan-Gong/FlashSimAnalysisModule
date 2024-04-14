from typing import List

from .analyzor import Analyzor
from ..data.time_series_data import *
from ..data import DataModel
from ..utility import GasField

class TimeSeriesAnalyzor(Analyzor):
    __tStartMyr: float = None
    __tEndMyr: float = None
    __tStepMyr: float = None
    __agnDataFileName: str = None
    __jetSmoothingMyr: int = None
    __timeSeriesData: TimeSeriesData
    

    def setTimeSpanKpc(self, tStartMyr: float, tEndMyr: float, tStepMyr: float):
        self.__tStartMyr = tStartMyr
        self.__tEndMyr = tEndMyr
        self.__tStepMyr = tStepMyr
        return self
    

    def setAgnDataFileName(self, agnDataFileName: str):
        self.__agnDataFileName = agnDataFileName
        return self
    

    def setJetSmoothingMyr(self, jetSmoothingMyr: int):
        self.__jetSmoothingMyr = jetSmoothingMyr
        return self
    

    def getData(self, rKpc: float) -> DataModel:
        self.__setTimeSeriesDataImpl()
        self.__timeSeriesData.setRadiusKpc(rKpc)
        return self.__timeSeriesData.getData()
    

    def getListOfData(self, rStartKpc, rEndKpc, rStepKpc) -> List[DataModel]:
        self.__setTimeSeriesDataImpl()
        listOfData: List[DataModel] = []
        for rKpc in range(rStartKpc, rEndKpc, rStepKpc):
            self.__timeSeriesData.setRadiusKpc(rKpc)
            listOfData.append(self.__timeSeriesData.getData())
        return listOfData
    

    def __setTimeSeriesDataImpl(self):
        self._checkBasicSetting()
        if (self.__tStartMyr is None or self.__tEndMyr is None or self.__tStepMyr is None):
            raise Exception("Please excute .setRadiusSpanKpc()")
        self.__timeSeriesData = self.__getTimeSeriesDataImpl()
        self.__timeSeriesData.setBasePath(self._basePath)
        self.__timeSeriesData.setHdf5FileTitle(self._hdf5Title)
        self.__timeSeriesData.setFileStepMyr(self._fileStepMyr)
        self.__timeSeriesData.setShape(self._shape)
        self.__timeSeriesData.setTimeSpanMyr(self.__tStartMyr, self.__tEndMyr, self.__tStepMyr)


    def __getTimeSeriesDataImpl(self) -> TimeSeriesData:
        if (self._gasProperty == GasField.Temperature or
            self._gasProperty == GasField.Pressure or
            self._gasProperty == GasField.Density or
            self._gasProperty == GasField.Entropy or
            self._gasProperty == GasField.Luminosity):
            return GasPropertyTimeSeriesData(self._gasProperty)
        elif (self._gasProperty == GasField.JetPower):
            jetPowerTsData = JetPowerTimeSeriesData()
            if (self.__jetSmoothingMyr is not None):
                jetPowerTsData.setSmoothingMyr(self.__jetSmoothingMyr)
            if (self.__agnDataFileName is not None):
                jetPowerTsData.setAgnDataFileName(self.__agnDataFileName)
            return jetPowerTsData
        elif (self._gasProperty == GasField.TurbulenceHeating):
            turbHeatingTs = TurbulenceHeatingTimeSeriesData()
            if (self._rhoIndex is not None):
                turbHeatingTs.setRhoIndex(self._rhoIndex)
            return turbHeatingTs
        else:
            raise Exception("This gas property does not support profile plot, please check the document")