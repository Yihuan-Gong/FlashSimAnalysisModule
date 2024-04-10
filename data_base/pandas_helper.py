from typing import List
import pandas as pd
import os

from .data_base_model import DataBaseModel

from ..utility import GasField


class PandasHelper():

    def writeDataIntoCsv(self, simBasePath : str, gasField : GasField, data : List[DataBaseModel]):
        filePath = self.__getFilePath(simBasePath, gasField)
        if (os.path.exists(filePath)):
            df = pd.read_csv(filePath)
        else:
            self.__createCsvDir(simBasePath)
            df = pd.DataFrame({
                'rKpc' : pd.Series(dtype='float'),
                'tMyr' : pd.Series(dtype='float'),
                'value' : pd.Series(dtype='float')
            })
        
        for pointData in data:
            df = df.append({
                'rKpc' : pointData.rKpc,
                'tMyr' : pointData.tMyr,
                'value' : pointData.value
            }, ignore_index=True)

        df.to_csv(filePath, index=False)
        del df


    def getDataFromCsv(self, simBasePath : str, gasField : GasField, rKpc : float, tMyr : float) -> float:
        filePath = self.__getFilePath(simBasePath, gasField)
        if (not os.path.exists(filePath)):
            return None
        df = pd.read_csv(filePath)
        result = df[(df['rKpc'] == rKpc) & (df['tMyr'] == tMyr)]['value'].to_list()
        del df
        if (len(result) == 0):
            return None
        else:
            return result[0]


    def resetDataBase(self, simBasePath : str, gasField : GasField):
        filePath = self.__getFilePath(simBasePath, gasField)
        if (not os.path.exists(filePath)):
            return
        os.remove(filePath)
        

    def __getFilePath(self, simBasePath : str, gasField : GasField):
        fieldName = f"{gasField}".split(".")[-1]
        return f"{simBasePath}/Csv/{fieldName}.csv"
    
    
    def __createCsvDir(self, simBasePath : str):
        fileDir = f"{simBasePath}/Csv/"
        if (not os.path.exists(fileDir)):
            os.makedirs(fileDir)