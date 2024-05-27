from typing import Callable, List, Tuple
from astropy import units as u
import pandas as pd
import os

from .db_model import DbModel
from ..enum.shape import Shape


class PandasHelper():
    '''
    PandasHelper can only read/write the database using DbModel
    '''
    
    def getDbFieldName(self, ytFieldName: Tuple[str, str]):
        return f"{ytFieldName[0]}_{ytFieldName[1]}"

    def writeDataIntoCsv(self, simBasePath : str, fieldName : str, shape: Shape, dbModelList: List[DbModel]):
        dfs = [self.__dbModelToDataFrame(dbModel) for dbModel in dbModelList]
        newDf = pd.concat(dfs, ignore_index=True)
        
        filePath = self.__getFilePath(simBasePath, fieldName, shape)
        if (os.path.exists(filePath)):
            df = pd.read_csv(filePath)
            # df = df.append(newDf, ignore_index=True)
            df = pd.concat([df, newDf], ignore_index=True)
        else:
            self.__createCsvDir(simBasePath)
            df = newDf

        df.to_csv(filePath, index=False)
        del df, newDf

    
    def getDataFromCsv(self, simBasePath : str, field : str, shape: Shape, 
                       rKpc : float, tMyr : float) -> pd.DataFrame:
        '''
        Return None if file not found, or file exist but no matching data found
        '''
        resultRow = self.__getData(simBasePath, field, shape, rKpc, tMyr)
        if (resultRow is None):
            return None
        if (len(resultRow) == 0):
            return None
        return resultRow
            # return resultRow['value'].to_list()[0]

    
    def getDataOrUpdateDb(
        self,
        simPath: str,
        dbFieldName: str,
        funcToGetValue: Callable[..., u.Quantity],
        rKpc: float,
        timeMyr: float,
        shape: Shape
    ) -> u.Quantity:
        '''
        This method get data from db if required data already exsit;
        calculate a new data and write to db if required does not exist.
        '''
        # Find the calculated result from data base
        data = self.getDataFromCsv(
            simBasePath=simPath, 
            field=dbFieldName,  
            shape=shape, 
            rKpc=rKpc, 
            tMyr=timeMyr
        )
        if (data is not None):
            value = data["value"].to_list()[0] * u.Unit(data["valueUnit"].to_list()[0])
            return value
        
        # If the calculated result does not exist in data base,
        # we calculate one here
        value = funcToGetValue()
        
        # Write the calculated result into data base
        PandasHelper().writeDataIntoCsv(
            simBasePath=simPath, 
            fieldName=dbFieldName,
            shape=shape,
            dbModelList=[DbModel(
                rKpc=rKpc, 
                tMyr=timeMyr, 
                value=float(value.value),
                valueUnit=value.unit
            )]
        )
        return value
    
    
    def resetDataBase(self, simBasePath : str, fieldName : str, shape: Shape):
        filePath = self.__getFilePath(simBasePath, fieldName, shape)
        if (not os.path.exists(filePath)):
            return
        os.remove(filePath)


    def __getData(self, simBasePath: str, fieldName: str, shape: Shape, rKpc: float, tMyr: float) -> pd.DataFrame:
        filePath = self.__getFilePath(simBasePath, fieldName, shape)
        if (not os.path.exists(filePath)):
            return None
        df = pd.read_csv(filePath)
        return df[(df['rKpc'] == rKpc) & (df['tMyr'] == tMyr)]
        

    def __getFilePath(self, simBasePath : str, fieldName : str, shape: Shape):
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