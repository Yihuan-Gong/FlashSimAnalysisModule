from ..utilities.velocity_filtering import (
    VelocityFiltering, 
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData2dReturnModel,
    VelocityFilteringMode,
    VelocityFilteringField
)
from ..utilities.density_filtering import (
    DensityFiltering,
    DensityFilteringCalculationInfoModel,
    DensityFilteringData2dReturnModel
)
from ..utilities.turbulence_heating_vazza import (
    TurbulenceHeatingVazza,
    TurbulenceHeatingVazzaCalculationInfoModel,
    TurbulenceHeatingVazzaData2dReturnModel,
    TurbulenceHeatingVazzaMode
)
from .methods.los_vel_dispersion import (
    LosVelDispersion,
    LosDispersionCalculationInfoModel,
    LosVelDispersionData2dReturnModel
)
from ....models import SimFileModel


class Data2dAnalyzor:
    
    def velocityFilteringByField(
            self, 
            field: VelocityFilteringField,
            axis: str,
            simFile: SimFileModel, 
            calculationInfo: VelocityFilteringCalculationInfoModel
        ) -> VelocityFilteringData2dReturnModel:
        return VelocityFiltering()\
            .setInputsByField(field, simFile, calculationInfo).getData2d(axis)
    
    
    def densityFiltering(
        self,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: DensityFilteringCalculationInfoModel
    ) -> DensityFilteringData2dReturnModel:
        return DensityFiltering().setInputs(simFile, calculationInfo).getData2d(axis)
    
    
    def turbulenceHeatingVazza(
        self,
        mode: TurbulenceHeatingVazzaMode,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel
    ) -> TurbulenceHeatingVazzaData2dReturnModel:
        return TurbulenceHeatingVazza()\
            .setInputs(mode, simFile, calculationInfo).getData2d(axis)
            
    
    def losVelDispersion(
        self,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: LosDispersionCalculationInfoModel
    ) -> LosVelDispersionData2dReturnModel: 
        return LosVelDispersion()\
            .setInputs(simFile, calculationInfo).getData2d(axis)