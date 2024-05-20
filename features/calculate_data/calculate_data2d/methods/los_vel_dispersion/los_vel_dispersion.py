import numpy as np
from typing import Dict, Tuple
from astropy import units as u

from .models import (
    LosDispersionCalculationInfoModel,
    LosVelDispersionData2dReturnModel
)
from ......utility import FieldAdder, CellCoorCalculator
from ......services import YtRawDataHelper, PickleService
from ......models import SimFileModel

class LosVelDispersion:
    __simFile: SimFileModel
    __calculationInfo: LosDispersionCalculationInfoModel
    __velocityFieldDict: Dict[str, str]
    __xrayFieldName: Tuple[str, str]
    __pickleService: PickleService


    def __init__(self) -> None:
        FieldAdder.AddFields()
    
    
    def setInputs(
        self, 
        simFile: SimFileModel, 
        calculationInfo: LosDispersionCalculationInfoModel
    ):
        self.__simFile = simFile
        self.__calculationInfo = calculationInfo
        self.__xrayFieldName = ("gas", "xray_emissivity_0.5_7.0_keV")
        self.__velocityFieldDict = {
            "x": calculationInfo.velxFieldName,
            "y": calculationInfo.velyFieldName,
            "z": calculationInfo.velzFieldName
        }
        self.__pickleService = PickleService(
            simPath=simFile.simPath,
            prefix=self.__class__.__name__,
            timeMyr=calculationInfo.timeMyr,
            rBoxKpc=calculationInfo.rBoxKpc
        )
        return self
    
    
    def getData2d(self, axis: str) -> LosVelDispersionData2dReturnModel:
        result = self.__pickleService.readFromFile()
        if (result != None):
            return result
        
        (cube, cubeDims) = self.__getRawDataCube(axis)
        velocityRawDataCube = cube[self.__velocityFieldDict[axis]].to_astropy() # is np.array
        xrayRawDataCube = cube[self.__xrayFieldName].to_astropy() # is np.array

        # Calculated losVelDispersionMap
        cubeLen = cubeDims[0]
        losVelDispersionMap: np.ndarray = np.zeros(shape=(cubeLen, cubeLen))
        for i in range(cubeLen):
            for j in range(cubeLen):
                losVelDispersionMap[i,j] = self.__calculateLosVelDispersion(\
                    i, j, axis, velocityRawDataCube.value, xrayRawDataCube.value
                )
        
        # Retrieve the coordinate for losVelDispersionMap
        axisCoorKpc: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=self.__simFile, 
            calculationInfo=self.__calculationInfo
        )
        axes = ["x", "y", "z"]
        axes.remove(axis)
        result = LosVelDispersionData2dReturnModel(
            value=losVelDispersionMap*velocityRawDataCube.unit,
            horizontalAxis=(axes[0], axisCoorKpc),
            verticalAxis=(axes[1], axisCoorKpc),
        )
        self.__pickleService.saveIntoFile(result)
        return result


    def __calculateLosVelDispersion(
            self, i: int, j: int, axis: str,
            velocityRawDataCube: np.ndarray,
            xrayRawDataCube: np.ndarray
        ) -> float:
        # Get los velocity and los xray emissivity
        losVelocity: np.ndarray
        losXrayEmissivity: np.ndarray
        if (axis == "z"):
            losVelocity = velocityRawDataCube[i,j,:]
            losXrayEmissivity = xrayRawDataCube[i,j,:]
        elif (axis == "x"):
            losVelocity = velocityRawDataCube[:,i,j]
            losXrayEmissivity = xrayRawDataCube[:,i,j]
        elif (axis == "y"):
            losVelocity = velocityRawDataCube[i,:,j]
            losXrayEmissivity = xrayRawDataCube[i,:,j]
        
        # Calculate los velocity dispersion weighted by xray emmisivity
        weightedAvgVel = 0.
        weightedAvgVelSquare = 0.
        totalLosXrayEmissivity = losXrayEmissivity.sum()
        for k in range(losVelocity.__len__()):
            weightedAvgVel += losVelocity[k] * losXrayEmissivity[k]/totalLosXrayEmissivity
            weightedAvgVelSquare += (losVelocity[k]**2.) * losXrayEmissivity[k]/totalLosXrayEmissivity
        return (weightedAvgVelSquare - weightedAvgVel**2.)**0.5


    def __getRawDataCube(self, axis: str):
        cube = YtRawDataHelper().loadRawData(
            simFile=self.__simFile,
            timeMyr=self.__calculationInfo.timeMyr,
            rBoxKpc=self.__calculationInfo.rBoxKpc,
            fields=[
                self.__xrayFieldName, 
                self.__velocityFieldDict[axis]
            ]
        )
        return cube  
