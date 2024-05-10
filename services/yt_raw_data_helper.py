from typing import List, Tuple
import yt
import numpy as np

from .yt_ds_helper import YtDsHelper
from ..models.sim_file_model import SimFileModel

class YtRawDataHelper:
    def loadRawData(
        self, 
        simFile: SimFileModel, 
        timeMyr: int, 
        rBoxKpc: float,
        fields: List[Tuple[str, str]]
    ) -> Tuple[
        yt.data_objects.construction_data_containers.YTCoveringGrid,
        List[int]
    ]:
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
            simFile=simFile,
            timeMyr=timeMyr,
            ionized=ionzied
        )
        if (ionzied):
            yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)

        # Extract all data points in ds and convert it from AMR to fixed grid
        low = yt.YTArray(np.array([-rBoxKpc, -rBoxKpc, -rBoxKpc]).astype(float), "kpc")
        maxlevel = ds.max_level
        cellSizeKpc = ds.domain_width.in_units("kpc").d  / (ds.domain_dimensions * 2**maxlevel)
        dims: int = np.ceil(-2*low.d / cellSizeKpc).astype(int)
        cube = ds.covering_grid(maxlevel, left_edge=low, dims=dims, fields=fields)
        return (cube, list(dims))

