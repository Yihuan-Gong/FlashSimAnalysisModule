from typing import List

from ..utility import GasField
from ..data.profile_data import *
from ..data import DataModel
from ..data_base import PandasHelper

class ProfileAnalyzor:
    __gasProperty: GasField = None
    __basePath: str = None
    __fileStepMyr: int = 1
    __rStartKpc: float = None
    __rEndKpc: float = None
    __rStepKpc: float = None
    __profileData: ProfileData = None


    def setField(self, gasField: GasField):
        self.__gasProperty = gasField
        return self

    
    def setBasePath(self, basePath: str):
        self.__basePath = basePath
        return self
    

    def setFileStepMyr(self, fileStepMyr: int):
        self.__fileStepMyr = fileStepMyr
        return self
    

    def setRadiusSpanKpc(self, rStartKpc: float, rEndKpc: float, rStepKpc: float):
        self.__rStartKpc = rStartKpc
        self.__rEndKpc = rEndKpc
        self.__rStepKpc = rStepKpc
        return self
    

    def getData(self, timeMyr: float) -> DataModel:
        self.__setProfileDataImpl()
        self.__profileData.setTimeMyr(timeMyr)
        return self.__profileData.getData()
    

    def getListOfData(self, timeStartMyr, timeEndMyr, timeStepMyr) -> List[DataModel]:
        self.__setProfileDataImpl()
        listOfData: List[DataModel] = []
        for timeMyr in range(timeStartMyr, timeEndMyr, timeStepMyr):
            self.__profileData.setTimeMyr(timeMyr)
            listOfData.append(self.__profileData.getData())
        return listOfData
    

    def resetDataBase(self):
        if (self.__basePath is None):
            raise Exception("You should excute .setBasePath() beforehand")
        if (self.__gasProperty is None):
            raise Exception("You should excute .setField() beforehand")
        PandasHelper().resetDataBase(self.__basePath, self.__gasProperty)
        return self


    def __checkInputCompleted(self):
        if (self.__gasProperty is None):
            raise Exception("Please excute .setField()")
        if (self.__basePath is None):
            raise Exception("Please excute .setBasePath()")
        if (self.__rStartKpc is None or self.__rEndKpc is None or self.__rStepKpc is None):
            raise Exception("Please excute .setRadiusSpanKpc()")
        
    
    def __setProfileDataImpl(self):
        self.__checkInputCompleted()
        self.__profileData = self.__getProfileDataImpl()
        self.__profileData.setBasePath(self.__basePath)
        self.__profileData.setFileStepMyr(self.__fileStepMyr)
        self.__profileData.setRadiusSpanKpc(self.__rStartKpc, self.__rEndKpc, self.__rStepKpc)


    def __getProfileDataImpl(self) -> ProfileData:
        if (self.__gasProperty == GasField.Temperature or
            self.__gasProperty == GasField.Pressure or
            self.__gasProperty == GasField.Density or
            self.__gasProperty == GasField.Entropy):
            return GasPropertyProfileData(self.__gasProperty)
        elif (self.__gasProperty == GasField.CoolingTime):
            return CoolingTimeProfileData()
        elif (self.__gasProperty == GasField.TurbulenceHeating):
            return TurbulenceHeatingProfileData()
        else:
            raise NotImplementedError("This gas property does not support profile plot, please check the document")


    