from dataclasses import dataclass

from ..enum.hdf5_mode import Hdf5Mode

@dataclass
class SimFileModel:
    simPath: str
    hdf5FileTitle: str
    hdf5FileMode: Hdf5Mode
    fileStepMyr: int