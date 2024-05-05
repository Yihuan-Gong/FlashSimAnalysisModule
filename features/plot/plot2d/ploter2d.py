from ..utility.hdf5_mode import Hdf5Mode

class Ploter2D:
    _simPath: str
    _hdf5FileTitle: str
    _hdf5FileMode: Hdf5Mode = Hdf5Mode.PlotFile
    _fileStepMyr: int

    def setFileProperties(self, simPath: str, hdf5Title: str, hdf5Mode: Hdf5Mode, fileStepMyr: int):
        self._simPath = simPath
        self._hdf5FileTitle = hdf5Title
        self._hdf5FileMode = hdf5Mode
        self._fileStepMyr = fileStepMyr
        return self
    