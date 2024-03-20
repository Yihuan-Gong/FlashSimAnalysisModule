import matplotlib.pyplot as plt
import pandas as pd
from python.modules.CoolingRateCalculator import CoolingRateCalculator

class PowerCurvePloter:
    solarMass = 1.9891e33
    Myr = 3.1557e13
    yr = 3.1557e7
    
    def __init__(self, basePath):
        self.basePath = basePath

    def PlotHeatingCurve(self, startTime, endTime, fileName = 'perseus_merger_agn_0000000000000001.dat'):
        header = pd.read_table(self.basePath + fileName, sep=', ', skiprows=[0], nrows=0, engine='python').columns
        datas = pd.read_table(self.basePath + fileName, sep="\s+", skiprows=[0,1], names=header)

        datas["Myr"] = datas['time (Myr)'] = datas['# time (s)']/self.Myr
        datas['jetpower (erg/s)'] = datas['energy (ergs)']/datas['dt(s)']

        filter1 = (datas['time (Myr)'] > startTime)
        filter2 = (datas['time (Myr)'] < endTime)
        filters = filter1 & filter2

        plt.plot(datas['time (Myr)'].loc[filters], 
                datas['jetpower (erg/s)'].loc[filters],
                label="Heating")

        plt.title("Jet Power")
        plt.xlabel("Time (Myr)")
        plt.ylabel("Jet power (erg/s)")
        plt.legend()
        plt.semilogy()
    

    def PlotCoolingCurve(self, startTime, endTime, step, regionSize):
        coolingRateCalculator = CoolingRateCalculator(self.basePath)
        (timeList, coolingRateList) = coolingRateCalculator.GetCoolingRateTimeSeries(
            startTime, endTime, step, regionSize
        )
        
        plt.plot(timeList, coolingRateList, label="Cooling")
        plt.title("X-ray radiative cooling")
        plt.xlabel("Time (Myr)")
        plt.ylabel("Cooling Rate (erg/s)")
        plt.legend()
        plt.semilogy()
    
    def PlotHeatingAndCoolingCurve(self, startTime, endTime, step, regionSize):
        self.PlotCoolingCurve(startTime, endTime, step, regionSize)
        self.PlotHeatingCurve(startTime, endTime)
        plt.title("Heating vs Cooling")
        plt.xlabel("Time (Myr)")
        plt.ylabel("Power (erg/s)")
        plt.legend()
        plt.semilogy()
