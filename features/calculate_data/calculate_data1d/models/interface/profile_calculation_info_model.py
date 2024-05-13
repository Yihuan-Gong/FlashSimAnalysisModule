from dataclasses import dataclass

@dataclass
class ProfileCalculationInfoModel:
    rStartKpc: float
    rEndKpc: float
    rStepKpc: float
    tMyr: float
    
    def getRList(self):
        return list(range(
            self.rStartKpc,
            self.rEndKpc,
            self.rStepKpc
        ))

