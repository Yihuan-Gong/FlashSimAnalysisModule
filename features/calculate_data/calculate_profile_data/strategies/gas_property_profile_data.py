import yt
from yt import derived_field
import numpy as np

from .profile_data import ProfileData
from ..models import GasPropertyProfileCalculationInfoModel
from .....models import Data1dReturnModel
from .....enum import GasField, Shape
from .....services.yt_ds_helper import YtDsHelper
from .....utility import FieldAdder
from .....utility.gas_field_unit_mapping import GasFieldUnitMapping
from .....utility.gas_field_yt_field_name_mapping import GasFieldYtFieldNameMapping

'''
    This class can only be used to plot
    1. Temperature profile
    2. Pressure profile
    3. Density profile
    4. Entropy profile
'''

class GasPropertyProfileData(ProfileData):
    __gasFieldName: str
    
    def __init__(self):
        super().__init__()
        FieldAdder.AddFields()

    
    def getData(self) -> Data1dReturnModel:
        calculationInfo: GasPropertyProfileCalculationInfoModel \
            = self._calculationInfo
        self.__gasFieldName = GasFieldYtFieldNameMapping().map(calculationInfo.gasProperty)
        
        if (calculationInfo.gasProperty == GasField.Luminosity):
            raise ValueError("So far GasField.Luminosity has not been developed yet. Please \
                use GasField.Emissivity at first and then do volume integral by your self.")
        
        profile = self.__getProfile(calculationInfo)
        return Data1dReturnModel(
            x = np.array(profile.x).tolist(),
            value = np.array(profile[self.__gasFieldName]).tolist(),
            valueUint=GasFieldUnitMapping().map(calculationInfo.gasProperty),
            label = (calculationInfo.tMyr/1000, "Gyr")
        )


    def __getProfile(self, calculationInfo: GasPropertyProfileCalculationInfoModel) \
        -> yt.Profile1D:
        ds: yt.DatasetSeries
        if (calculationInfo.gasProperty == GasField.Emissivity):
            ds = YtDsHelper().loadDs(
                simFile=self._simFile,
                timeMyr=calculationInfo.tMyr,
                ionized=True
            )
            yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
        else:
            ds = YtDsHelper().loadDs(
                simFile=self._simFile,
                timeMyr=calculationInfo.tMyr,
            )
        # sp = ds.sphere('c', (calculationInfo.rEndKpc, 'kpc'))
        ds.add_field(
            ("gas", "box_radius"), 
            function=self.__boxR, 
            sampling_type='cell',
            units='kpc',
            force_override=True
        )
        radiusField = ("gas", "radius") if calculationInfo.shape == Shape.Sphere else ("gas", "box_radius")
        numberOfDatas = int((calculationInfo.rEndKpc - calculationInfo.rStartKpc)/calculationInfo.rStepKpc)
        profile = yt.Profile1D(
            data_source=YtDsHelper().loadRegionFromDs(ds, calculationInfo.shape, calculationInfo.rEndKpc), 
            x_field=radiusField, 
            x_n=numberOfDatas, 
            x_min=calculationInfo.rStartKpc, 
            x_max=calculationInfo.rEndKpc, 
            x_log=calculationInfo.isLogR, 
            weight_field=calculationInfo.weightFieldName
        )
        profile.add_fields(self.__gasFieldName)
        del ds
        return profile
    
    
    # @derived_field(name=("gas", "box_radius"), units="kpc", sampling_type="cell")
    def __boxR(self, field, data):
        return np.maximum(
            data[("gas", "x")].d, 
            data[("gas", "y")].d, 
            data[("gas", "z")].d
        )*yt.YTQuantity(1., "cm")
