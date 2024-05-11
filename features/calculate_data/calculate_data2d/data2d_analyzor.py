from ..utilities.velocity_filtering import (
    VelocityFiltering, 
    VelocityFilteringCalculationInfoModel,
    VelocityFilteringData2dReturnModel,
    VelocityFilteringMode
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
    
    def velocityFiltering(
            self, 
            mode: VelocityFilteringMode,
            axis: str,
            simFile: SimFileModel, 
            calculationInfo: VelocityFilteringCalculationInfoModel
        ) -> VelocityFilteringData2dReturnModel:
        return VelocityFiltering()\
            .setInputs(mode, simFile, calculationInfo).getData2d(axis)
    
    
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