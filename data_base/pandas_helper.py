from typing import List, Tuple
import pandas as pd
import os
from typing import Callable

from .db_model import DbModel
from ..utility import GasField, Shape

'''
    PandasHelper can only read/write the database using DbModel
'''
class PandasHelper():

    def writeDataIntoCsv(self, simBasePath : str, gasField : GasField, shape: Shape, dbModelList: List[DbModel]):
        dfs = [self.__dbModelToDataFrame(dbModel) for dbModel in dbModelList]
        newDf = pd.concat(dfs, ignore_index=True)
        
        filePath = self.__getFilePath(simBasePath, gasField, shape)
        if (os.path.exists(filePath)):
            df = pd.read_csv(filePath)
            df = df.append(newDf, ignore_index=True)
        else:
            self.__createCsvDir(simBasePath)
            df = newDf

        df.to_csv(filePath, index=False)
        del df, newDf

    '''
        Return None if file not found, or file exist but no matching data found
    '''
    def getDataFromCsv(self, simBasePath : str, gasField : GasField, shape: Shape, 
                       rKpc : float, tMyr : float) -> pd.DataFrame:
        resultRow = self.__getData(simBasePath, gasField, shape, rKpc, tMyr)
        if (resultRow is None):
            return None
        if (len(resultRow) == 0):
            return None
        return resultRow
            # return resultRow['value'].to_list()[0]

    
    def resetDataBase(self, simBasePath : str, gasField : GasField, shape: Shape):
        filePath = self.__getFilePath(simBasePath, gasField, shape)
        if (not os.path.exists(filePath)):
            return
        os.remove(filePath)


    def __getData(self, simBasePath: str, gasField: GasField, shape: Shape, rKpc: float, tMyr: float) -> pd.DataFrame:
        filePath = self.__getFilePath(simBasePath, gasField, shape)
        if (not os.path.exists(filePath)):
            return None
        df = pd.read_csv(filePath)
        return df[(df['rKpc'] == rKpc) & (df['tMyr'] == tMyr)]
        

    def __getFilePath(self, simBasePath : str, gasField : GasField, shape: Shape):
        fieldName = f"{gasField}".split(".")[-1]
        shapeName = f"{shape}".split(".")[-1]
        return f"{simBasePath}/Csv/{fieldName}_{shapeName}.csv"
    
    
    def __createCsvDir(self, simBasePath : str):
        fileDir = f"{simBasePath}/Csv/"
        if (not os.path.exists(fileDir)):
            os.makedirs(fileDir)

    
    def __dbModelToDataFrame(self, dbModel: DbModel) -> pd.DataFrame:
        if (type(dbModel.value) == int or type(dbModel.value) == float):
            return pd.DataFrame.from_dict([dbModel.__dict__])
        else:
            df = pd.DataFrame.from_dict([dbModel.value.__dict__])
            df.insert(0, "rKpc", dbModel.rKpc)
            df.insert(1, "tMyr", dbModel.tMyr)
            return df