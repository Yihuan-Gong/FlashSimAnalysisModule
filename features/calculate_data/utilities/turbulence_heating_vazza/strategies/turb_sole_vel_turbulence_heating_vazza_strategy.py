from .turbulence_heating_vazza_strategy import TurbulenceHeatingVazzaStrategy
from ..models import (
    TurbulenceHeatingVazzaData3dReturnModel
)
from ...velocity_filtering import (
    VelocityFilteringMode,
)


class TurbSoleVelTurbulenceHeatingVazzaStrategy(
    TurbulenceHeatingVazzaStrategy
):
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        self._initVelocityFilter(VelocityFilteringMode.TurbCompSole)
        velFilteringResult = self._velocityFilter.getData3d()
        heatingPerMass = self._calculateHeatingPerMass(
            velocity=velFilteringResult.turbSoleVtotal,
            scale=velFilteringResult.scale
        )
        result = TurbulenceHeatingVazzaData3dReturnModel(
            xAxis=velFilteringResult.xAxis,
            yAxis=velFilteringResult.yAxis,
            zAxis=velFilteringResult.zAxis,
            heatingPerMass=heatingPerMass,
            heatingPerVolume=self._calculateHeatingPerVolume(heatingPerMass),
            scale=velFilteringResult.scale
        )
        self._pickleService.saveIntoFile(result)
        return result
        
    