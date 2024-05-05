from typing import Dict, Tuple
from ..enum.gas_field import GasField

class GasFieldYtFieldNameMapping:
    __gasFieldYtFieldNameDict: Dict[GasField, Tuple[str, str]]
    
    def __init__(self) -> None:
        self.__gasFieldYtFieldNameDict = {
            GasField.Density: ('gas', 'density'),
            GasField.Temperature: ('gas', 'temp_in_keV'),
            GasField.Pressure: ('gas', 'pressure'),
            GasField.Entropy: ('gas', 'entropy'),
            GasField.Luminosity: ("gas","xray_luminosity_0.5_7.0_keV"),
            GasField.Emissivity: ("gas","xray_emissivity_0.5_7.0_keV")
        }
        
    
    def map(self, gasField: GasField) -> Tuple[str, str]:
        return self.__gasFieldYtFieldNameDict[gasField]