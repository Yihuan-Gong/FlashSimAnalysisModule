import yt

from .shape import Shape

class YtDsHelper:
    
    def loadDs(self, simPath: str, fileTitle: str, timeMyr: int, fileStepMyr: int) -> yt.DatasetSeries:
        return yt.load(self.__getHdf5Path(simPath, fileTitle, timeMyr, fileStepMyr))
    

    def loadRegion(self, simPath: str, fileTitle: str, shape: Shape, rKpc: float, 
                   timeMyr: int, fileStepMyr: int):
        ds = self.loadDs(simPath, fileTitle, timeMyr, fileStepMyr)
        return self.loadRegionFromDs(ds, shape, rKpc)
    

    def loadRegionFromDs(self, ds: yt.DatasetSeries, shape: Shape, rKpc: float):
        if (shape == Shape.Sphere):
            return ds.sphere("c", yt.YTQuantity(rKpc, "kpc"))
        elif (shape == Shape.Box):
            return ds.box(
                yt.YTArray([-rKpc, -rKpc, -rKpc], "kpc"),
                yt.YTArray([rKpc, rKpc, rKpc], "kpc")
            )


    def __getHdf5Path(self,  simPath: str, fileTitle: str, timeMyr: int, fileStepMyr: int):
        return "%s/%s_hdf5_plt_cnt_%04d"%(simPath, fileTitle, timeMyr/fileStepMyr)
