import yt
import numpy as np
from typing import List, Tuple
from .data2d import Data2D
from .data2d_return_model import Data2dReturnModel
from ..utility.field_adder import FieldAdder
from ..utility.yt_raw_data_helper import YtRawDataHelper

class LosVelDispersionData2d(Data2D):
    __velocityFieldName: Tuple[str, str]
    __xrayFieldName: Tuple[str, str]


    def __init__(self) -> None:
        super().__init__()
        FieldAdder.AddFields()
        

    def getData(self) -> Data2dReturnModel:
        self.__velocityFieldName = ("gas", f"velocity_{self._data2dInputModel.axis}")
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
        axes.remove(self._data2dInputModel.axis)
        return Data2dReturnModel(
            value=np.flipud(losVelDispersionMap.transpose()),
            horizontalAxis=(axes[0], axisCoorKpc),
            verticalAxis=(axes[1], axisCoorKpc)
        )


    def __calculateLosVelDispersion(self, i, j, velocityRawDataCgsCube: np.ndarray,
                                    xrayRawDataCgsCube: np.ndarray) -> float:
        # Get los velocity and los xray emissivity
        losVelocity: np.ndarray
        losXrayEmissivity: np.ndarray
        if (self._data2dInputModel.axis == "z"):
            losVelocity = velocityRawDataCgsCube[i,j,:]
            losXrayEmissivity = xrayRawDataCgsCube[i,j,:]
        elif (self._data2dInputModel.axis == "x"):
            losVelocity = velocityRawDataCgsCube[:,i,j]
            losXrayEmissivity = xrayRawDataCgsCube[:,i,j]
        elif (self._data2dInputModel.axis == "y"):
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
            simPath=self._data2dInputModel.simPath,
            fileTitle=self._data2dInputModel.hdf5FileTitle,
            timeMyr=self._data2dInputModel.timeMyr,
            fileStepMyr=self._data2dInputModel.fileStepMyr,
            fields=[
                self.__xrayFieldName, 
                self.__velocityFieldName,
                ("gas", "x"),
            ],
            sizeKpc=self._data2dInputModel.sizeKpc,
            hd5fMode=self._data2dInputModel.hdf5FileMode
        )
        return cube  
