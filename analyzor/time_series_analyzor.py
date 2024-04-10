from typing import List

from ..data.time_series_data import *
from ..data import DataModel
from ..data_base import PandasHelper
from ..utility import GasField

class TimeSeriesAnalyzor:
    __gasProperty: GasField = None
    __basePath: str = None
    __fileStepMyr: int = 1
    __tStartMyr: float = None
    __tEndMyr: float = None
    __tStepMyr: float = None
    __agnDataFileName: str = None
    __jetSmoothingMyr: int = None
    __timeSeriesData: TimeSeriesData
    

    def setField(self, gasField: GasField):
        self.__gasProperty = gasField
        return self


    def setBasePath(self, basePath: str):
        self.__basePath =  basePath
        return self

    
    def setFileStepMyr(self, fileStepMyr: int):
        self.__fileStepMyr = fileStepMyr
        return self
    

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



    def resetDataBase(self):
        if (self.__basePath is None):
            raise Exception("You should excute .setBasePath() beforehand")
        PandasHelper().resetDataBase(self.__basePath, self.__gasProperty)
        return self
    


    def __setTimeSeriesDataImpl(self):
        self.__checkInputCompleted()
        self.__timeSeriesData = self.__getTimeSeriesDataImpl()
        self.__timeSeriesData.setBasePath(self.__basePath)
        self.__timeSeriesData.setFileStepMyr(self.__fileStepMyr)
        self.__timeSeriesData.setTimeSpanMyr(self.__tStartMyr, self.__tEndMyr, self.__tStepMyr)


    def __checkInputCompleted(self):
        if (self.__gasProperty is None):
            raise Exception("Please excute .setField()")
        if (self.__basePath is None):
            raise Exception("Please excute .setBasePath()")
        if (self.__tStartMyr is None or self.__tEndMyr is None or self.__tStepMyr is None):
            raise Exception("Please excute .setRadiusSpanKpc()")


    def __getTimeSeriesDataImpl(self) -> TimeSeriesData:
        if (self.__gasProperty == GasField.Temperature or
            self.__gasProperty == GasField.Pressure or
            self.__gasProperty == GasField.Density or
            self.__gasProperty == GasField.Entropy or
            self.__gasProperty == GasField.Luminosity):
            return GasPropertyTimeSeriesData(self.__gasProperty)
        elif (self.__gasProperty == GasField.JetPower):
            jetPowerTsData = JetPowerTimeSeriesData()
            if (self.__jetSmoothingMyr is not None):
                jetPowerTsData.setSmoothingMyr(self.__jetSmoothingMyr)
            if (self.__agnDataFileName is not None):
                jetPowerTsData.setAgnDataFileName(self.__agnDataFileName)
            return jetPowerTsData
        elif (self.__gasProperty == GasField.TurbulenceHeating):
            return TurbulenceHeatingTimeSeriesData()
        else:
            raise Exception("This gas property does not support profile plot, please check the document")