from typing import Dict, Tuple
from ..enum.gas_field import GasField

class GasFieldUnitMapping:
    __gasFieldUnitDict: Dict[GasField, str]
    
    def __init__(self) -> None:
        self.__gasFieldUnitDict = {
            GasField.Density: "g/cm^3",
            GasField.Temperature: "keV",
            GasField.Pressure: "Ba",
            GasField.Entropy: "keV*cm^2",
            GasField.Luminosity: "erg/s"
        }
    
    
    def map(self, gasField: GasField) -> str:
        return self.__gasFieldUnitDict[gasField]