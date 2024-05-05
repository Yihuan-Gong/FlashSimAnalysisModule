import yt
from typing import List

from .time_series_data import TimeSeriesData
from ..models.gas_property_time_series_calculation_info_model import GasPropertyTimeSeriesCalculationInfoModel
from .....data_base import PandasHelper
from .....data_base import DbModel
from .....enum.gas_field import GasField
from .....models.data1d_return_model.data1d_return_model import Data1dReturnModel
from .....services.yt_ds_helper import YtDsHelper
from .....utility.field_adder import FieldAdder
from .....utility.gas_field_yt_field_name_mapping import GasFieldYtFieldNameMapping
from .....utility.gas_field_unit_mapping import GasFieldUnitMapping


class GasPropertyTimeSeriesData(TimeSeriesData):
    t: range
    fileNums: List[int]
    
    
    def __init__(self) -> None:
        super().__init__()
        FieldAdder.AddFields()
    

    def getData(self) -> Data1dReturnModel:
        '''
            Return: Data1dReturnModel(
                x: List[float],            # time in Myr
                value: List[float],  
                valueUnit: str             #unit of the time series
                label: Tuple[float, str]   # (r, unit of r)
            )
        '''
        calculationInfo: GasPropertyTimeSeriesCalculationInfoModel \
            = self._calculationInfo
        self.t = range(
            calculationInfo.tStartMyr,
            calculationInfo.tEndMyr,
            calculationInfo.tStepMyr
        )
        self.fileNums = [int(x/self._simFile.fileStepMyr) for x in self.t]
        return Data1dReturnModel(
            x=self.t,
            value=self.__getTimeSeries(calculationInfo),
            valueUint=GasFieldUnitMapping().map(calculationInfo.gasProperty),
            label=(self._calculationInfo.rKpc, "kpc")
        )
    

    def __getTimeSeries(self, calculationInfo: GasPropertyTimeSeriesCalculationInfoModel):
        timeSeries = []
        for timeMyr in self.t:
            value: float # The field value at the specific (r, t)
            # Find the calculated result from data base
            data = PandasHelper().getDataFromCsv(
                self._simFile.simPath, 
                f"{calculationInfo.gasProperty}".split(".")[-1],
                calculationInfo.shape, 
                calculationInfo.rKpc, 
                timeMyr
            )
            if (data is not None):
                value = data["value"].to_list()[0]
                timeSeries.append(value)
                continue
            
            # If the calculated result does not exist in data base,
            # we calculate one here
            gasFieldName = GasFieldYtFieldNameMapping().map(calculationInfo.gasProperty)
            if (calculationInfo.gasProperty == GasField.Luminosity):
                ds = YtDsHelper().loadDs(self._simFile, timeMyr, True)
                # ds = yt.load('%s/%s_hdf5_plt_cnt_%04d'%(self.basePath, self.hdf5FileTitle, timeMyr/self.fileStepMyr),
                #              default_species_fields="ionized")
                yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
                region = YtDsHelper().loadRegionFromDs(ds, calculationInfo.shape, calculationInfo.rKpc)
                value = float(region.quantities.total_quantity(gasFieldName).d)
            else:
                region = YtDsHelper().loadRegion(self._simFile, calculationInfo.shape, calculationInfo.rKpc, timeMyr)
                value = float(region.quantities.weighted_average_quantity(gasFieldName, calculationInfo.weightFieldName).d)
            del region

            # Write the calculated result into data base
            timeSeries.append(value)
            PandasHelper().writeDataIntoCsv(
                self._simFile.simPath, 
                f"{calculationInfo.gasProperty}".split(".")[-1],
                calculationInfo.shape,
                [DbModel(calculationInfo.rKpc, timeMyr, value)]
            )
        return timeSeries
    
    