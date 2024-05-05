from typing import List

from .profile_data import ProfileData
from ..models import TurbulenceHeatingProfileCalculationInfoModel
from .....models import TurbDataReturnModel, Data1dReturnModel
from .....utility.turbulence_analyzor import TurbulenceAnalyzor
from .....data_base import TurbPandasHelper, DbModel, TurbDbModel
from .....services.yt_ds_helper import YtDsHelper
from .....enum import Shape

class TurbulenceHeatingProfileData(ProfileData):
    def __init__(self) -> None:
        super().__init__()
    
    
    def getData(self) -> Data1dReturnModel:
        calculationInfo: TurbulenceHeatingProfileCalculationInfoModel \
            = self._calculationInfo
        
        if (calculationInfo.shape != Shape.Box):
            raise ValueError("Turbulence heating only support box shape!")
        return Data1dReturnModel(
            x = self._r,
            value = self.__getProfile(calculationInfo),
            valueUint="erg/s",
            label = (calculationInfo.tMyr/1000, "Gyr")
        )
    
    
    def __getProfile(self, calculationInfo: TurbulenceHeatingProfileCalculationInfoModel) \
        -> TurbDataReturnModel:
        turbDataList: List[TurbDbModel] = []
        for rKpc in self._r:
            turbData = TurbPandasHelper().getTurbDataFromCsv(
                simBasePath=self._simFile.simPath,
                shape=calculationInfo.shape,
                rKpc=rKpc,
                tMyr=calculationInfo.tMyr,
                rhoIndex=calculationInfo.rhoIndex
            )
            if (turbData is not None):
                turbDataList.append(turbData)
                continue
            
            ds = YtDsHelper().loadDs(
                simFile=self._simFile,
                timeMyr=calculationInfo.tMyr
            )
            turbDataTemp = TurbulenceAnalyzor() \
                .setDensityWeightingIndex(calculationInfo.rhoIndex) \
                .setDataSeries(ds) \
                .setBoxSize(rKpc) \
                .calculatePowerSpectrum() \
                .getDissipationRate()
            turbData = TurbDbModel(
                rhoIndex=calculationInfo.rhoIndex,
                upperLimit=turbDataTemp["turb_heating_rate_upper_limit"],
                lowerLimit=turbDataTemp["turb_heating_rate_lower_limit"]
            )
            turbDataList.append(turbData)
            TurbPandasHelper().writeDataIntoCsv(
                simBasePath=self._simFile.simPath,
                field="TurbulenceHeating", 
                shape=calculationInfo.shape,
                dbModelList=[DbModel(
                    rKpc=rKpc, 
                    tMyr=calculationInfo.tMyr, 
                    value=turbData
                )]
            )

        return TurbDataReturnModel(
            rhoIndex=calculationInfo.rhoIndex,
            upperLimit=[x.upperLimit for x in turbDataList],
            lowerLimit=[x.lowerLimit for x in turbDataList]
        )
    