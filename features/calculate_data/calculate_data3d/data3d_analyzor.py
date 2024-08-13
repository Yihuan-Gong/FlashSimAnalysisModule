from ..utilities.velocity_filtering import (
    VelocityFiltering, 
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData3dReturnModel,
    VelocityFilteringMode,
    VelocityFilteringField
)
from ..utilities.turbulence_heating_vazza import (
    TurbulenceHeatingVazza,
    TurbulenceHeatingVazzaCalculationInfoModel,
    TurbulenceHeatingVazzaData3dReturnModel,
    TurbulenceHeatingVazzaMode
)
from ..utilities.density_filtering import (
    DensityFiltering,
    DensityFilteringCalculationInfoModel,
    DensityFilteringData3dReturnModel
)
from ..utilities.yt_field import (
    YtField,
    YtFieldCalculationInfoModel,
    YtFieldData3dReturnModel
)
from ....models import SimFileModel

class Data3dAnalyzor:
    
    ytField = YtField()
    
    def velocityFiltering(
            self, 
            mode: VelocityFilteringMode,
            simFile: SimFileModel, 
            calculationInfo: VelocityFilteringCalculationInfoModel
        ) -> VelocityFilteringData3dReturnModel:
        return VelocityFiltering()\
            .setInputs(mode, simFile, calculationInfo).getData3d()
    
    
    def velocityFilteringByField(
        self, 
        field: VelocityFilteringField,
        simFile: SimFileModel, 
        calculationInfo: VelocityFilteringCalculationInfoModel
    ) -> VelocityFilteringData3dReturnModel:
        return VelocityFiltering()\
            .setInputsByField(field, simFile, calculationInfo).getData3d()
    
    
    def densityFiltering(
        self,
        simFile: SimFileModel,
        calculationInfo: DensityFilteringCalculationInfoModel
    ) -> DensityFilteringData3dReturnModel:
        return DensityFiltering().setInputs(simFile, calculationInfo).getData3d()
    
    
    def turbulenceHeatingVazza(
        self,
        mode: TurbulenceHeatingVazzaMode,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    ) -> TurbulenceHeatingVazzaData3dReturnModel:
        return TurbulenceHeatingVazza()\
            .setInputs(mode, simFile, calculationInfo).getData3d()
    
    
    