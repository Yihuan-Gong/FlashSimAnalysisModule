from ..utilities.velocity_filtering import (
    VelocityFiltering, 
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData2dReturnModel,
    VelocityFilteringMode
)
from ....models import SimFileModel

class Data2dAnalyzor:
    
    def velocityFiltering(
            self, 
            mode: VelocityFilteringMode,
            axis: str,
            simFile: SimFileModel, 
            calculationInfo: VelocityFilteringCalculationInfoModel
        ) -> VelocityFilteringData2dReturnModel:
        return VelocityFiltering()\
            .setInputs(mode, simFile, calculationInfo)\
            .getData2d(axis)