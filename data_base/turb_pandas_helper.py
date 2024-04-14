from .pandas_helper import PandasHelper
from .db_model import DbModel
from .turb_db_model import TurbDbModel
from ..utility import GasField, Shape

class TurbPandasHelper(PandasHelper):

    def getTurbDataFromCsv(
            self, simBasePath : str, shape: Shape, 
            rKpc : float, tMyr : float, rhoIndex: float
        ) -> TurbDbModel:

        data = self.getDataFromCsv(
            simBasePath, 
            GasField.TurbulenceHeating, 
            shape, 
            rKpc, 
            tMyr
        )
        if (data is None):
            return None

        data = data[data["rhoIndex"] == rhoIndex]
        if (len(data) == 0):
            return None
        
        return TurbDbModel(
            rhoIndex=rhoIndex,
            upperLimit=data["upperLimit"].to_list()[0],
            lowerLimit=data["lowerLimit"].to_list()[0]
        )
        