from dataclasses import dataclass

@dataclass
class JetPowerTimeSeriesCalculationInfoModel:
    tStartMyr: float
    tEndMyr: float
    smoothingMyr: float = None
    agnDataFileName: str = "perseus_merger_agn_0000000000000001.dat"