import yt

from .shape import Shape
from ..utility.hdf5_mode import Hdf5Mode

class YtDsHelper:
    
    def loadDs(self, simPath: str, fileTitle: str, timeMyr: int, fileStepMyr: int, 
               hd5fMode: Hdf5Mode = Hdf5Mode.PlotFile, ionized: bool = False) -> yt.DatasetSeries:
        if (ionized):
            return yt.load(self.__getHdf5Path(simPath, fileTitle, hd5fMode, timeMyr, fileStepMyr), default_species_fields="ionized")
        else:
            return yt.load(self.__getHdf5Path(simPath, fileTitle, hd5fMode, timeMyr, fileStepMyr))
    

    def loadRegion(self, simPath: str, fileTitle: str, shape: Shape, rKpc: float, 
                   timeMyr: int, fileStepMyr: int, hd5fMode: Hdf5Mode = Hdf5Mode.PlotFile):
        ds = self.loadDs(simPath, fileTitle, timeMyr, fileStepMyr, hd5fMode)
        return self.loadRegionFromDs(ds, shape, rKpc)
    

    def loadRegionFromDs(self, ds: yt.DatasetSeries, shape: Shape, rKpc: float):
        if (shape == Shape.Sphere):
            return ds.sphere("c", yt.YTQuantity(rKpc, "kpc"))
        elif (shape == Shape.Box):
            return ds.box(
                yt.YTArray([-rKpc, -rKpc, -rKpc], "kpc"),
                yt.YTArray([rKpc, rKpc, rKpc], "kpc")
            )


    def __getHdf5Path(self,  simPath: str, fileTitle: str, hdf5Mode: Hdf5Mode, timeMyr: int, fileStepMyr: int):
        modeStrMapping = {
            Hdf5Mode.PlotFile: "hdf5_plt_cnt",
            Hdf5Mode.CheckPointFile: "hdf5_chk",
            Hdf5Mode.ForcePlot: "forced_hdf5_plt_cnt"
        }
        return f"{simPath}/{fileTitle}_{modeStrMapping[hdf5Mode]}_{int(timeMyr/fileStepMyr):04d}"
# %(simPath, fileTitle, modeStrMapping[hdf5Mode], timeMyr/fileStepMyr)
        
