from dataclasses import dataclass
from typing import Tuple
import yt

@dataclass
class XrayCalculationInfo:
    minBandKeV: float = 0.5
    maxBandKeV: float = 7
    tableType: str = "apec"
    metallicity: float = 0.3
    
    def getXrayEmissivityFieldName(self) -> Tuple[str, str]:
        return ("gas",f"xray_emissivity_{self.minBandKeV}_{self.maxBandKeV}_keV")
    
    def getXrayLuminosityFieldName(self) -> Tuple[str, str]:
        return ("gas",f"xray_luminosity_{self.minBandKeV}_{self.maxBandKeV}_keV")
    
    def addXrayFields(self, ds: any):
        '''
        ds: yt.DataSeries
        '''
        yt.add_xray_emissivity_field(ds, self.minBandKeV, self.maxBandKeV, table_type=self.tableType, metallicity=self.metallicity)