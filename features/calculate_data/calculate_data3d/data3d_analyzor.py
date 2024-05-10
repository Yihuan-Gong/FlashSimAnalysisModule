from ..utilities.velocity_filtering import (
    VelocityFiltering, 
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData3dReturnModel,
    VelocityFilteringMode
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
            .setInputs(mode, simFile, calculationInfo)\
            .getData3d()
    
    
    