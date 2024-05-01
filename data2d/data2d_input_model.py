from dataclasses import dataclass

from ..utility.hdf5_mode import Hdf5Mode

@dataclass
class Data2dInputModel:
    simPath: str
    hdf5FileTitle: str
    hdf5FileMode: Hdf5Mode
    fileStepMyr: int
    axis: str
    sizeKpc: float
    timeMyr: int