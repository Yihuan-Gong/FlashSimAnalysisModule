import pickle
import os
from typing import Any

class PickleService:
    __simPath: str
    __prefix: str
    __timeMyr: int
    __rBoxKpc: int
    
    
    def __init__(self, simPath: str, prefix: str, timeMyr: int, rBoxKpc: int) -> None:
        self.__simPath = simPath
        self.__prefix = prefix
        self.__timeMyr = timeMyr
        self.__rBoxKpc = rBoxKpc
    
    
    def saveIntoFile(self, object: Any):
        dir = self.__getFileDir()
        if (not os.path.exists(dir)):
            os.makedirs(dir)
        with open(self.__getFilePath(), "wb") as file:
            pickle.dump(object, file)
    
    
    def readFromFile(self) -> Any:
        '''
        Return object if file exist
        Returb None if file does not exist
        '''
        path = self.__getFilePath()
        if (not os.path.exists(path)):
            return None
        result: Any
        with open(path, "rb") as file:
            result = pickle.load(file)
        return result
    
    
    def __getFilePath(self) -> str:
        path = f"{self.__getFileDir()}/{self.__timeMyr:04d}Myr_{self.__rBoxKpc}kpc.pkl"
        return path
    
    
    def __getFileDir(self):
        return f"{self.__simPath}/analysis_objects/{self.__prefix}/"