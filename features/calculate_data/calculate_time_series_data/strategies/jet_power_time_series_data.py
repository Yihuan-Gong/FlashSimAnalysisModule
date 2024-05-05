import pandas as pd

from .time_series_data import TimeSeriesData
from ..models.jet_power_time_series_calculation_info_model import JetPowerTimeSeriesCalculationInfoModel
from .....models.data1d_return_model.data1d_return_model import Data1dReturnModel
from .....utility import Constants

class JetPowerTimeSeriesData(TimeSeriesData):

    def __init__(self) -> None:
        super().__init__()


    def getData(self) -> Data1dReturnModel:
        '''
            Return: Data1dReturnModel(
                x: List[float],      # time in Myr
                value: List[float],  # jet power in erg/s
                valueUnit: str       # "erg/s"
                label: None
            )
        '''
        calculationInfo: JetPowerTimeSeriesCalculationInfoModel = self._calculationInfo
        agnFilePath = f"{self._simFile.simPath}/{self._simFile.hdf5FileTitle}_{calculationInfo.agnDataFileName}"
        
        header = pd.read_table(agnFilePath, sep=', ', skiprows=[0], nrows=0, engine='python').columns
        datas = pd.read_table(agnFilePath, sep="\s+", skiprows=[0,1], names=header)
        datas["Myr"] = datas['time (Myr)'] = datas['# time (s)']/Constants.Myr
        datas['jetpower (erg/s)'] = datas['energy (ergs)']/datas['dt(s)']

        if (calculationInfo.smoothingMyr is not None):
            datas["MyrGroup"] = (datas["Myr"]//calculationInfo.smoothingMyr)
            groupedData = datas.groupby("MyrGroup").mean()
            filter1 = (groupedData['time (Myr)'] > self._calculationInfo.tStartMyr)
            filter2 = (groupedData['time (Myr)'] < self._calculationInfo.tEndMyr)
            filters = filter1 & filter2
            return Data1dReturnModel(
                x=groupedData['time (Myr)'].loc[filters].tolist(),
                value=groupedData['jetpower (erg/s)'].loc[filters].tolist(),
                valueUint="erg/s",
                label=None
            )
        
        filter1 = (datas['time (Myr)'] > self._calculationInfo.tStartMyr)
        filter2 = (datas['time (Myr)'] < self._calculationInfo.tEndMyr)
        filters = filter1 & filter2
        return Data1dReturnModel(
            x=datas['time (Myr)'].loc[filters].tolist(),
            value=datas['jetpower (erg/s)'].loc[filters].tolist(),
            valueUint="erg/s",
            label=None
        )
    