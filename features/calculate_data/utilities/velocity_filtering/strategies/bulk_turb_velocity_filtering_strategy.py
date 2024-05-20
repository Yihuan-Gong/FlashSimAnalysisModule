from typing import Tuple, List
from astropy import units as u
import mirpyidl as idl
import numpy as np

from .velocity_filtering_strategy import VelocityFilteringStrategy
from ..model import (
    VelocityFilteringData2dReturnModel,
    VelocityFilteringData3dReturnModel
)
from ......services import YtRawDataHelper
from ......utility import DataConverter, CellCoorCalculator

class BulkTurbVelocityFilteringStrategy\
    (VelocityFilteringStrategy):
    
    def getData2d(self, axis: str) -> VelocityFilteringData2dReturnModel:
        result = self.getData3d()
        turbVtotal: u.Quantity = self._calculateTotalVelocity(
            result.turbVx, result.turbVy, result.turbVz)
        axes = DataConverter().data3dTo2dGetAxisName(axis)
        return VelocityFilteringData2dReturnModel(
            turbVx=DataConverter().data3dTo2dMiddle(result.turbVx, axis),
            turbVy=DataConverter().data3dTo2dMiddle(result.turbVy, axis),
            turbVz=DataConverter().data3dTo2dMiddle(result.turbVz, axis),
            turbVtotal=DataConverter().data3dTo2dMiddle(turbVtotal, axis),
            scaleCells=DataConverter().data3dTo2dMiddle(result.scaleCells, axis),
            scale=DataConverter().data3dTo2dMiddle(result.scale, axis),
            horizontalAxis=(axes[0], result.xAxis),
            verticalAxis=(axes[1], result.yAxis)
        )
        
    
    def getData3d(self) -> VelocityFilteringData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        (self._cube, self._cubeDims) = self._getVelocityRawDataCube()
        (turbVelVector, scaleScalar) = self.__idlBridgeVelocityFiltering()
        turbVtotal: np.ndarray = np.sqrt(\
            turbVelVector[0]**2 + \
            turbVelVector[1]**2 + \
            turbVelVector[1]**2
        )
        cellCoor: u.Quantity = CellCoorCalculator().getAxisCoor(
            simFile=self._simFile, calculationInfo=self._calculationInfo
        )
        cellSize: u.Quantity = cellCoor[1] - cellCoor[0]
        result = VelocityFilteringData3dReturnModel(
            xAxis=cellCoor,
            yAxis=cellCoor,
            zAxis=cellCoor,
            turbVx=turbVelVector[0] * u.cm/u.s,
            turbVy=turbVelVector[1] * u.cm/u.s,
            turbVz=turbVelVector[2] * u.cm/u.s,
            turbVtotal=turbVtotal * u.cm/u.s,
            scaleCells=scaleScalar,
            scale=scaleScalar*cellSize
        )
        self._pickleService.saveIntoFile(result)
        return result
    
    
    def __idlBridgeVelocityFiltering(self) \
        -> Tuple[List[np.ndarray], np.ndarray]:
        '''
        Returns
        1. turbVelocityVector: List[np.ndarray] => [turbVx, turbVy, turbVz]
        2. scale: np.ndarray
        '''
        velxFlat = self.__getIdlFormatFieldValue(self._calculationInfo.velxFieldName)
        velyFlat = self.__getIdlFormatFieldValue(self._calculationInfo.velyFieldName)
        velzFlat = self.__getIdlFormatFieldValue(self._calculationInfo.velzFieldName)
        
        turbVelVector: List[np.ndarray] = []
        scaleVector: List[np.ndarray] = []
        # scale: 
        for velFlat in [velxFlat, velyFlat, velzFlat]:
            try:
                # Pass the 1D array to IDL
                idl.setVariable('n', self._cubeDims[0])
                # Reshape to 3D array
                idl.setVariable('vel1D', velFlat)
                 # Run IDL filering script
                # idl.execute("vel = reform(vel1D, n, n, n)")
                idl.execute("vel = vel1D")
                idl.execute(self.__getIdlCode())
            except idl.IdlArithmeticError:
                pass
        
            # Get result back from IDL
            velTurb = idl.getVariable('turbo')
            scale    = idl.getVariable('scale')

            # Append to turb_v_component
            turbVelVector.append(velTurb)
            scaleVector.append(scale)
        
        # Convert scale into scalar from vector
        scaleScalar = np.sqrt(scaleVector[0]**2 + scaleVector[1]**2 + scaleVector[2]**2)
        return (turbVelVector, scaleScalar)
    
    
    def __getIdlFormatFieldValue(self, fieldName) -> np.ndarray:
        return self._cube[fieldName].d
    
    
    def __getIdlCode(self):
        r2: str = "uint(n*0.5-1.)" if self._calculationInfo.bulkTurbFilteringMaxScale == None\
            else self._calculationInfo.bulkTurbFilteringMaxScale
        r1: str = self._calculationInfo.bulkTurbFilteringMinScale
        eps: str = self._calculationInfo.bulkTurbFilteringEps
        return f" \
            r2={r2}   &\
            r1={r1}    &\
            turbo=fltarr(n,n,n)    &\
            scale=fltarr(n,n,n)    &\
            sk=fltarr(n,n,n)    &\
            scale(*,*,*)= 0.    &\
            eps={eps}    &\
            nk=8    &\
            epssk=1.    &\
            drr=1.    &\
            meanv = smooth(vel,nk,/EDGE_TRUNCATE)   &\
            sc = abs((vel-meanv)/vel)   &\
            kernel=MAKE_ARRAY(nk,nk,nk, /float, value =1.)   &\
            kernel(0,*,*) = 0.   &\
            kernel(*,0,*) = 0.   &\
            kernel(*,*,0) = 0.   &\
            kernel(nk-1,*,*) = 0.   &\
            kernel(*,nk-1,*) = 0.   &\
            kernel(*,*,nk-1) = 0.   &\
            sk=convol((vel-meanv)^2,kernel,/edge_truncate,/normalize)   &\
            sk=meanv^3/float(sk^1.5)   &\
            sc1 = 0    &\
            for r=r1,r2,drr do begin   &\
                print,r   &\
                width = 2.*r+1    &\
                meanv = smooth(vel,width,/EDGE_TRUNCATE)   &\
                sc = abs((vel-meanv)/vel)    &\
                skm=smooth(sk,width,/EDGE_TRUNCATE)    &\
                ibox=where((abs(sc-sc1)/float(sc1) lt eps or abs(skm) gt epssk) and scale eq 0.,nn)   &\
                if nn gt 0 then begin   &\
                    turbo(ibox)=vel(ibox)-meanv(ibox)    &\
                    scale(ibox) = float(r+0.01)    &\
                endif   &\
                sc1=sc   &\
            endfor   \
        "
    
    
    