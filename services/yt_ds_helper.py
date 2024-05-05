import yt

from ..enum.shape import Shape
from ..enum.hdf5_mode import Hdf5Mode
from ..models.sim_file_model import SimFileModel

class YtDsHelper:
    
    def loadDs(self, simFile: SimFileModel, timeMyr: int, ionized: bool = False) -> yt.DatasetSeries:
        if (ionized):
            return yt.load(self.__getHdf5Path(simFile, timeMyr), default_species_fields="ionized")
        else:
            return yt.load(self.__getHdf5Path(simFile, timeMyr,))
    

    def loadRegion(self, simFile: SimFileModel, shape: Shape, rKpc: float, timeMyr: int):
        ds = self.loadDs(simFile, timeMyr)
        return self.loadRegionFromDs(ds, shape, rKpc)
    

    def loadRegionFromDs(self, ds: yt.DatasetSeries, shape: Shape, rKpc: float):
        if (shape == Shape.Sphere):
            return ds.sphere("c", yt.YTQuantity(rKpc, "kpc"))
        elif (shape == Shape.Box):
            return ds.box(
                yt.YTArray([-rKpc, -rKpc, -rKpc], "kpc"),
                yt.YTArray([rKpc, rKpc, rKpc], "kpc")
            )


    def __getHdf5Path(self, simFile: SimFileModel, timeMyr: int):
        modeStrMapping = {
            Hdf5Mode.PlotFile: "hdf5_plt_cnt",
            Hdf5Mode.CheckPointFile: "hdf5_chk",
            Hdf5Mode.ForcePlot: "forced_hdf5_plt_cnt"
        }
        return f"{simFile.simPath}/{simFile.hdf5FileTitle}_{modeStrMapping[simFile.hdf5FileMode]}_{int(timeMyr/simFile.fileStepMyr):04d}"
# %(simPath, fileTitle, modeStrMapping[hdf5Mode], timeMyr/fileStepMyr)
        
