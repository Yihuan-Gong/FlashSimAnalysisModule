from typing import List, Tuple
import yt
import numpy as np

from .yt_ds_helper import YtDsHelper
from .hdf5_mode import Hdf5Mode

class YtRawDataHelper:

    def loadRawData(self, simPath: str, fileTitle: str, timeMyr: int, fileStepMyr: int, 
                    fields: List[Tuple[str, str]], sizeKpc: float, hd5fMode: Hdf5Mode = Hdf5Mode.PlotFile) \
                    -> yt.data_objects.construction_data_containers.YTCoveringGrid:
        '''
        Return:
        1. 3D raw data from hdf5 file. Type: yt.data_objects.construction_data_containers.YTCoveringGrid
        2. The dimension of YTCoveringGrid. Type: List[int]
        '''
        # Get yt.DataSeries from hdf5 file
        ionzied: bool = False
        if (fields.__contains__(("gas", "xray_emissivity_0.5_7.0_keV")) or \
            fields.__contains__(("gas", "xray_luminosity_0.5_7.0_keV"))):
            ionzied = True
        ds = YtDsHelper().loadDs(
            simPath=simPath,
            fileTitle=fileTitle,
            timeMyr=timeMyr,
            fileStepMyr=fileStepMyr,
            hd5fMode=hd5fMode,
            ionized=ionzied
        )
        if (ionzied):
            yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)

        # Extract all data points in ds and convert it from AMR to fixed grid
        low = yt.YTArray([-sizeKpc/2., -sizeKpc/2., -sizeKpc/2.], "kpc")
        maxlevel = ds.max_level
        cellSizeKpc = ds.domain_width.in_units("kpc").d  / (ds.domain_dimensions * 2**maxlevel)
        dims = np.ceil(-2*low.d / cellSizeKpc).astype(int)
        cube = ds.covering_grid(maxlevel, left_edge=low, dims=dims, fields=fields)
        return (cube, list(dims))

