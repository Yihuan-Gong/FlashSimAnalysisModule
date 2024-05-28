from typing import Iterable, List, Tuple
from astropy import units as u
import numpy as np

from ..models import ProfileReturnModel
from .....services import AstropyService



class Converter:
    
    def data3dToProfile(
        self, 
        array3d: u.Quantity, 
        rKpcList: Iterable[float], 
        coor: u.Quantity
    ) -> Tuple[u.Quantity, u.Quantity]:
        '''
        Transform box 3d array (n*n*n) into profile according to coordinate of each cell
        data3d: 3d array with shape (n,n,n)
        coor: 1d array with length n
        '''
        coorX, coorY, coorZ = np.meshgrid(
            coor, coor, coor, indexing="ij")
        r:u.Quantity = np.sqrt(coorX**2 + coorY**2 + coorZ**2).to("kpc")
        
        # Get a (n,n,n) array. The value of each element is the index at rKpcList
        binIndices = np.digitize(r.value, rKpcList)

        binnedValues: List[u.Quantity] = []
        binRanges: List[float] = []
        for i in range(1, len(rKpcList)):
            binMask = binIndices == i
            if np.any(binMask):
                binnedValues.append(array3d[binMask].mean())
                binRanges.append((rKpcList[i-1]+rKpcList[i])/2)
        
        return (
            u.Quantity(binRanges, "kpc"),
            AstropyService().quantityListToQuantity(binnedValues)
        )
    
    
    def sphereIntegral(self, perVolumeData: ProfileReturnModel) -> ProfileReturnModel:
        '''
        The integration starts from perVolumeData.rKpcList[0] and ends
        at perVolumeData.rKpcList[-1]. So please request the perVolumeData
        from rKpc=0.
        '''
        # From rMin to rMax
        r = u.Quantity(perVolumeData.rKpcList, "kpc")
        dr: u.Quantity = r[1]-r[0]
        rInner: u.Quantity = r - dr/2.
        rOuter: u.Quantity = r + dr/2.
        dV: u.Quantity = 4./3.*np.pi*(rOuter**3-rInner**3)
        integratedProf = np.cumsum(perVolumeData.yValue*dV).cgs
        
        return ProfileReturnModel(
            timeMyr=perVolumeData.timeMyr,
            shape=perVolumeData.shape,
            rKpcList=perVolumeData.rKpcList,
            yValue=integratedProf
        )
        