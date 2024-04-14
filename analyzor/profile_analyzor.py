from typing import List

from .analyzor import Analyzor
from ..utility import GasField
from ..data.profile_data import *
from ..data import DataModel

class ProfileAnalyzor(Analyzor):
    __rStartKpc: float = None
    __rEndKpc: float = None
    __rStepKpc: float = None
    __profileData: ProfileData = None
    

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

    
    def __setProfileDataImpl(self):
        self._checkBasicSetting()
        if (self.__rStartKpc is None or self.__rEndKpc is None or self.__rStepKpc is None):
            raise Exception("Please excute .setRadiusSpanKpc()")
        self.__profileData = self.__getProfileDataImpl()
        self.__profileData.setBasePath(self._basePath)
        self.__profileData.setHdf5FileTitle(self._hdf5Title)
        self.__profileData.setFileStepMyr(self._fileStepMyr)
        self.__profileData.setShape(self._shape)
        self.__profileData.setRadiusSpanKpc(self.__rStartKpc, self.__rEndKpc, self.__rStepKpc)


    def __getProfileDataImpl(self) -> ProfileData:
        if (self._gasProperty == GasField.Temperature or
            self._gasProperty == GasField.Pressure or
            self._gasProperty == GasField.Density or
            self._gasProperty == GasField.Entropy):
            return GasPropertyProfileData(self._gasProperty)
        elif (self._gasProperty == GasField.CoolingTime):
            return CoolingTimeProfileData()
        elif (self._gasProperty == GasField.TurbulenceHeating):
            turbHeatingProfile = TurbulenceHeatingProfileData()
            if (self._rhoIndex is not None):
                turbHeatingProfile.setRhoIndex(self._rhoIndex)
            return turbHeatingProfile
        else:
            raise NotImplementedError("This gas property does not support profile plot, please check the document")


    