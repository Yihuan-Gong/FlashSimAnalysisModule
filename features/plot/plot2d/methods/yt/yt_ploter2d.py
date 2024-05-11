from typing import List
import yt
import numpy as np
import os

from ......utility.field_adder import FieldAdder
from ......enum import YtPloter2DMode
from ......services.yt_ds_helper import YtDsHelper

class YtPloter2D(Ploter2D):
    __plot: any = None


    def __init__(self):
        FieldAdder.AddFields()


    def plot(self):
        '''
        You must perform .setFileProperties() and .setBasicPlotProperties() before excuting this function
        '''
        ds = YtDsHelper().loadDs(
            simPath=self._simPath,
            fileTitle=self._hdf5FileTitle,
            timeMyr=self.__timeMyr,
            fileStepMyr=self._fileStepMyr,
            hd5fMode=self._hdf5FileMode,
            ionized=self.__ionized
        )
        if (self.__field == "cray_density" or self.__field == ("gas", "cray_density")):
            self.__addCrFields(ds)
        elif(self.__field == ("gas", "xray_emissivity_0.5_7.0_keV")):
            yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
        
        if (self.__plotMode == YtPloter2DMode.Slice):
            self.__plot = yt.SlicePlot(
                ds,
                self.__axis,
                self.__field,
                center=self.__center,
                width= (self.__sizeKpc, "kpc")
            )
        elif (self.__plotMode == YtPloter2DMode.Projection):
            self.__plot = yt.ProjectionPlot(
                ds,
                self.__axis,
                self.__field,
                center=self.__center,
                width= (self.__sizeKpc, "kpc")
            )
        self.__plot.set_cmap(self.__field, 'Blue-Red')
        self.__plot.annotate_text(
            [0.05,0.95],
            'time = %.3f Gyr' %ds.current_time.in_units('Gyr'),
            coord_system='axis',text_args={'color':'black'}
        )
        self.__additionalMarking()
        ds.close()
        return self
    

    def show(self):
        if (self.__plot == None):
            raise Exception("You should excute .plot() at first")
        self.__plot.show()
        return self
    

    def getYtPlotObject(self):
        if (self.__plot == None):
            raise Exception("You should excute .plot() at first")
        return self.__plot
    

    def savePlot(self, path: str):
        if (self.__plot == None):
            raise Exception("You should excute .plot() at first")
        (saveDir, name) = os.path.split(path)
        if (not os.path.exists(saveDir)):
            os.makedirs(saveDir)
        self.__plot.save(f"{saveDir}/{name}")
        return self
    

    def close(self):
        pass


    def setBasicPlotProperties(self, mode: YtPloter2DMode, timeMyr: int, sizeKpc: float, axis: str, field):
        self.__plotMode = mode
        self.__timeMyr = timeMyr
        self.__sizeKpc = sizeKpc
        self.__axis = axis
        self.__field = field
        if (field == "xray" or
            field == "xray_emissivity" or 
            field == ("gas", "xray_emissivity_0.5_7.0_keV")):
            field = ("gas", "xray_emissivity_0.5_7.0_keV")
            self.__ionized = True
        return self
    

    def setZlim(self, zlimMin, zlimMax):
        self.__zlimMin = zlimMin
        self.__zlimMax = zlimMax
        return self
    

    def setCenter(self, center: yt.YTArray):
        self.__center = center
        return self
    

    def markPoint(self, markPointPos):
        self.__markPointPos = markPointPos
        return self
    
    
    def markContour(self, contour: str, countourNum: int = 20):
        self.__contour = contour
        self.__contourNum = countourNum
        return self
    

    def markVelocity(self, velocityScale: float = 1e10):
        self.__markVelocity = True
        self.__velocityScale = velocityScale
        return self
    

    def markGrid(self):
        self.__markGrid = True
        return self
    

    def __additionalMarking(self):
        if (self.__zlimMin != None):
            self.__plot.set_zlim(self.__field, self.__zlimMin, self.__zlimMax)
        if self.__markGrid:
            self.__plot.annotate_grids()
        if self.__contour is not None:
            self.__plot.annotate_contour(self.__contour, ncont=self.__contourNum)
        for oneMarker in self.__markPointPos:
            self.__plot.annotate_marker(oneMarker, coord_system="plot")
        if self.__markParticles:
            self.__plot.annotate_particles((self.__sizeKpc, "kpc"))
        if self.__markVelocity:
            self.__plot.annotate_velocity(scale=self.__velocityScale)


    def __addCrFields(self, ds: yt.DatasetSeries):
        if (('flash', 'cray') in ds.field_list):
            ds.add_field(
                ('gas', 'cray_density'), 
                function=self.__crayVolumeDensity, 
                sampling_type='cell',
                units='erg*cm**(-3)',
                force_override=True
            )

    
    def __crayVolumeDensity(self, field, data):
        return np.maximum((data["cray"].d)*(data["density"].d), 1e-15)*yt.YTQuantity(1., "erg*cm**(-3)")
