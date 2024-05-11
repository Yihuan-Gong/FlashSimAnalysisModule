from ..utilities.velocity_filtering import (
    VelocityFiltering, 
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData3dReturnModel,
    VelocityFilteringMode
)
from ..utilities.turbulence_heating_vazza import (
    TurbulenceHeatingVazza,
    TurbulenceHeatingVazzaCalculationInfoModel,
    TurbulenceHeatingVazzaData3dReturnModel,
    TurbulenceHeatingVazzaMode
)
from ....models import SimFileModel

class Data3dAnalyzor:

    def velocityFiltering(
            self, 
            mode: VelocityFilteringMode,
            simFile: SimFileModel, 
            calculationInfo: VelocityFilteringCalculationInfoModel
        ) -> VelocityFilteringData3dReturnModel:
        return VelocityFiltering()\
            .setInputs(mode, simFile, calculationInfo).getData3d()
            
    
    def turbulenceHeatingVazza(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    ) -> TurbulenceHeatingVazzaData3dReturnModel:
        return TurbulenceHeatingVazza()\
            .setInputs(mode, simFile, calculationInfo).getData3d()
    
    
    