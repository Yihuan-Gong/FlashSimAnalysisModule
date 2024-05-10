import yt

from ..enum.shape import Shape
from ..models.sim_file_model import SimFileModel

class YtDsHelper:
    
    def loadDs(self, simFile: SimFileModel, timeMyr: int, ionized: bool = False) -> yt.DatasetSeries:
        if (ionized):
            return yt.load(simFile.getHdf5Path(timeMyr), default_species_fields="ionized")
        else:
            return yt.load(simFile.getHdf5Path(timeMyr))
    

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

        
