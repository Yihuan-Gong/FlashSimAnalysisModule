from .turbulence_heating_vazza_strategy import TurbulenceHeatingVazzaStrategy
from ..models import (
    TurbulenceHeatingVazzaData3dReturnModel
)
from ...velocity_filtering import (
    VelocityFilteringMode,
)

class SimonteVelTurbulenceHeatingVazzaStrategy(
    TurbulenceHeatingVazzaStrategy
):
    def getData3d(self) -> TurbulenceHeatingVazzaData3dReturnModel:
        result = self._pickleService.readFromFile()
        if (result != None):
            return result
        
        # Calculate scale
        self._initVelocityFilter(VelocityFilteringMode.BulkTurb)
        scale = self._velocityFilter.getData3d().scale
        
        # Calculate Simonte velocity
        self._initVelocityFilter(VelocityFilteringMode.Simonte)
        velFilteringResult = self._velocityFilter.getData3d()
        
        # Calculate heating per mass
        heatingPerMass = self._calculateHeatingPerMass(
            velocity=velFilteringResult.simonteVtotal,
            scale=scale
        )
        
        result = TurbulenceHeatingVazzaData3dReturnModel(
            xAxis=velFilteringResult.xAxis,
            yAxis=velFilteringResult.yAxis,
            zAxis=velFilteringResult.zAxis,
            heatingPerMass=heatingPerMass,
            heatingPerVolume=self._calculateHeatingPerVolume(heatingPerMass),
            scale=scale
        )
        self._pickleService.saveIntoFile(result)
        return result
        