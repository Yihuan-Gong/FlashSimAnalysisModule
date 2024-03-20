import yt

class CoolingRateCalculator:
    def __init__(self, basePath):
        self.basePath = basePath

    def GetCoolingRateTimeSeries(self, startTime, endTime, step, region):
        timeList = range(startTime, endTime, step)
        coolingRateList = []
        for time in timeList:
            coolingRateList.append(self.GetCoolingRate(time, region))
        return (timeList, coolingRateList)

    def GetCoolingRate(self, time, region):
        # Read data
        filePath = '%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, time)
        ds = yt.load(filePath, default_species_fields="ionized")
        ray_fields = yt.add_xray_emissivity_field(ds, 0.5, 7.0, table_type='apec', metallicity=0.3)

        # Calculate luminosity in each region
        sp = ds.sphere("c", (region, "kpc"))
        luminosity = sp.quantities.total_quantity(("gas","xray_luminosity_0.5_7.0_keV"))
        
        return luminosity
    
    