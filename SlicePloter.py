import yt
import numpy as np
from python.modules.utility.field_adder import FieldAdder

class SlicePloter:
    
    def __init__(self, basePath):
        FieldAdder.AddFields()
        self.basePath = basePath

    def Plot(self, num, L=8 ,chkFile=False, forcePlot=False, 
             axis='z', field=("gas", "temp_in_keV"), sliceCenter = [0,0,0], markCenterPos = [(0,0)],
             setZlim=False, min=0.8, max=15, contour=None, n_contour=20, grid = False, markCenter = False, 
             particles = False, velocity = False, velocityScale=1e10):

        hd5fPath: str
        if (chkFile):
            hd5fPath = '%s/perseus_merger_hdf5_chk_%04d'%(self.basePath, num)
        elif (forcePlot):
            hd5fPath = '%s/perseus_merger_forced_hdf5_plt_cnt_%04d'%(self.basePath, num)
        else:
            hd5fPath = '%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, num)
        
        ds: yt.DatasetSeries
        if (field == "xray" or
            field == "emissivity" or 
            field == "xray_emissivity" or 
            field == ("gas", "xray_emissivity_0.5_7.0_keV")):
            field = ("gas", "xray_emissivity_0.5_7.0_keV")
            ds = yt.load(hd5fPath, default_species_fields="ionized")
            yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)
        else:
            ds = yt.load(hd5fPath)

        if (field == "cray_density" or field == ("gas", "cray_density")):
            self.__addCrFields(ds)
        
        p = yt.SlicePlot(
            ds, 
            axis, 
            field,
            center = sliceCenter,
            width = (L, 'Mpc')
        )
        p.set_cmap(field, 'Blue-Red')
        if (setZlim):
            p.set_zlim(field, min, max)
        p.annotate_text([0.05,0.95],'time = %.3f Gyr' %ds.current_time.in_units('Gyr'),coord_system='axis',text_args={'color':'black'})
        
        if grid:
            p.annotate_grids()

        if contour is not None:
            p.annotate_contour(contour, ncont=n_contour)

        if markCenter:
            for oneMarker in markCenterPos:
                p.annotate_marker(oneMarker, coord_system="plot")
        
        if particles:
            p.annotate_particles((L, "Mpc"))
        
        if velocity:
            p.annotate_velocity(scale=velocityScale)

        p.show()

        del ds
        del p
    

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
