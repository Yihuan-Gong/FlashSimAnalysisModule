import pandas as pd
from astropy import units as u

from .models import JetPowerTimeSeriesCalculationInfoModel
from ...models import TimeSeriesReturnModel
from ......models import SimFileModel
from ......utility import Constants

class JetPowerData1d:

    def getTimeSeriesData(
        self,
        simFile: SimFileModel,
        calculationInfo: JetPowerTimeSeriesCalculationInfoModel
    ) -> TimeSeriesReturnModel:
        agnFilePath = f"{simFile.simPath}/{calculationInfo.agnDataFileName}"
        
        header = pd.read_table(agnFilePath, sep=', ', skiprows=[0], nrows=0, engine='python').columns
        datas = pd.read_table(agnFilePath, sep="\s+", skiprows=[0,1], names=header)
        datas["Myr"] = datas['time (Myr)'] = datas['# time (s)']/Constants.Myr
        datas['jetpower (erg/s)'] = datas['energy (ergs)']/datas['dt(s)']

        if (calculationInfo.smoothingMyr is not None):
            datas["MyrGroup"] = (datas["Myr"]//calculationInfo.smoothingMyr)
            datas = datas.groupby("MyrGroup").mean(numeric_only=True)
        
        filter1 = (datas['time (Myr)'] > calculationInfo.tStartMyr)
        filter2 = (datas['time (Myr)'] < calculationInfo.tEndMyr)
        filters = filter1 & filter2
        return TimeSeriesReturnModel(
            rKpc=None,
            shape=None,
            timeMyrList=datas['time (Myr)'].loc[filters].tolist(),
            yValue=datas['jetpower (erg/s)'].loc[filters].tolist()*u.Unit("erg/s")
        )
