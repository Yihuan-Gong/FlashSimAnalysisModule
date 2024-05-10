import numpy as np
from typing import List, Tuple

from .data2d import Data2d
from ..models.data2d_return_model import Data2dReturnModel
from .....utility.field_adder import FieldAdder
from .....services.yt_raw_data_helper import YtRawDataHelper

class LosVelDispersionData2d(Data2d):
    __velocityFieldName: Tuple[str, str]
    __xrayFieldName: Tuple[str, str]


    def __init__(self) -> None:
        super().__init__()
        FieldAdder.AddFields()
    
    
    def getData(self) -> Data2dReturnModel:
        self.__velocityFieldName = ("gas", f"velocity_{self._calculationInfo.axis}")
        self.__xrayFieldName = ("gas", "xray_emissivity_0.5_7.0_keV")
        (cube, cubeDims) = self.__getRawDataCube()
        velocityRawDataCgsCube = cube[self.__velocityFieldName].d # is np.array
        xrayRawDataCgsCube = cube[self.__xrayFieldName].d # is np.array

        # Calculated losVelDispersionMap
        cubeLen = cubeDims[0]
        losVelDispersionMap: np.ndarray = np.zeros(shape=(cubeLen, cubeLen))
        for i in range(cubeLen):
            for j in range(cubeLen):
                losVelDispersionMap[i,j] = self.__calculateLosVelDispersion(\
                    i, j, velocityRawDataCgsCube, xrayRawDataCgsCube
                )
        
        # Retrieve the coordinate for losVelDispersionMap
        axisCoorKpc = (cube[("gas", "x")].in_units("kpc").d)[:,0,0]
        axes = ["x", "y", "z"]
        axes.remove(self._calculationInfo.axis)
        return Data2dReturnModel(
            value=np.flipud(losVelDispersionMap.transpose()),
            horizontalAxis=(axes[0], axisCoorKpc),
            verticalAxis=(axes[1], axisCoorKpc),
            axisUnit="kpc"
        )


    def __calculateLosVelDispersion(self, i, j, velocityRawDataCgsCube: np.ndarray,
                                    xrayRawDataCgsCube: np.ndarray) -> float:
        # Get los velocity and los xray emissivity
        losVelocity: np.ndarray
        losXrayEmissivity: np.ndarray
        if (self._calculationInfo.axis == "z"):
            losVelocity = velocityRawDataCgsCube[i,j,:]
            losXrayEmissivity = xrayRawDataCgsCube[i,j,:]
        elif (self._calculationInfo.axis == "x"):
            losVelocity = velocityRawDataCgsCube[:,i,j]
            losXrayEmissivity = xrayRawDataCgsCube[:,i,j]
        elif (self._calculationInfo.axis == "y"):
            losVelocity = velocityRawDataCgsCube[i,:,j]
            losXrayEmissivity = xrayRawDataCgsCube[i,:,j]
        
        # Calculate los velocity dispersion weighted by xray emmisivity
        weightedAvgVel = 0.
        weightedAvgVelSquare = 0.
        totalLosXrayEmissivity = losXrayEmissivity.sum()
        for k in range(losVelocity.__len__()):
            weightedAvgVel += losVelocity[k] * losXrayEmissivity[k]/totalLosXrayEmissivity
            weightedAvgVelSquare += (losVelocity[k]**2.) * losXrayEmissivity[k]/totalLosXrayEmissivity
        return (weightedAvgVelSquare - weightedAvgVel**2.)**0.5


    def __getRawDataCube(self):
        cube = YtRawDataHelper().loadRawData(
            simFile=self._simFile,
            timeMyr=self._calculationInfo.timeMyr,
            rBoxKpc=self._calculationInfo.rBoxKpc,
            fields=[
                self.__xrayFieldName, 
                self.__velocityFieldName,
                ("gas", "x"),
            ]
        )
        return cube  
