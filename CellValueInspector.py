import yt
import numpy as np
from python.modules.utility.field_adder import FieldAdder


class CellValueInspector:

    def __init__(self, basePath):
        self.basePath = basePath

    def __readFile(self, num, chkFile=False, forcedPlot=False):
        FieldAdder.AddFields()
        if (chkFile):
            ds = yt.load('%s/perseus_merger_hdf5_chk_%04d'%(self.basePath, num))
        elif (forcedPlot):
            ds = yt.load('%s/perseus_merger_forced_hdf5_plt_cnt_%04d'%(self.basePath, num))
        else:
            ds = yt.load('%s/perseus_merger_hdf5_plt_cnt_%04d'%(self.basePath, num))
        return ds
    
    def __rho(self, P, T):
        amu = 1.6605e-24
        kB  = 1.3807e-16
        return P*amu/(kB*T)


    def __findExtremaIndex(self, ds, rMin=0, r=8, mainField="density"):
        kpc = 3.0857e21
        
        solnData = ds.covering_grid(6, yt.YTArray([-r,-r,-r], "kpc"), r*2, [mainField, ("gas", "x"), ("gas", "y"), ("gas", "z")])
        excluded = (solnData[("gas", "x")]**2. + solnData[("gas", "y")]**2. + solnData[("gas", "z")]**2.) < (rMin*kpc)**2.

        solnData[mainField][excluded] = 0.
        (iMax, jMax, kMax) = np.unravel_index(np.argmax(solnData[mainField]), solnData[mainField].shape)

        solnData[mainField][excluded] = np.inf
        (iMin, jMin, kMin) = np.unravel_index(np.argmin(solnData[mainField]), solnData[mainField].shape)
        return ((iMax, jMax, kMax), (iMin, jMin, kMin))
    

    def __getValueAtIndex(self, ds, index = (0,0,0), r=8, fields=["density"]):
        solnData = ds.covering_grid(6, yt.YTArray([-r,-r,-r], "kpc"), r*2, fields)

        valueList = []
        for field in fields:
            valueList.append(solnData[field][index[0], index[1], index[2]])
        
        if ("temperature" in fields and "pressure" in fields and "density" in fields):
            P = solnData["pressure"][index[0], index[1], index[2]]
            T = solnData["temperature"][index[0], index[1], index[2]]
            rhoActural = solnData["density"][index[0], index[1], index[2]]
            valueList.append(self.__rho(P, T)/rhoActural)

        return valueList
    
    def __getPosAtIndex(self, ds, index = (0,0,0), r=8):
        solnData = ds.covering_grid(
            6, yt.YTArray([-r,-r,-r], "kpc"), r*2, 
            [("gas", "x"), ("gas", "y"), ("gas", "z")]
        )
        
        return yt.YTArray([
            solnData[("gas", "x")][index[0], index[1], index[2]],
            solnData[("gas", "y")][index[0], index[1], index[2]],
            solnData[("gas", "z")][index[0], index[1], index[2]],
        ]).in_units("kpc")
    

    # Public
    def FindOtherFieldsAtExtremaOfMainFeild(
        self, num, rMin=0, r=8, chkFile=False, forcedPlot=False,
        mainField="density", otherFields=[]
    ):
    
        ds = self.__readFile(num, chkFile, forcedPlot)
        fields = [mainField] + otherFields

        (maxIndex, minIndex) = self.__findExtremaIndex(ds, r=r, rMin=rMin, mainField=mainField)
        
        posMax = self.__getPosAtIndex(ds, maxIndex, r)
        posMin = self.__getPosAtIndex(ds, minIndex, r)

        maxList = [posMax] + self.__getValueAtIndex(ds, maxIndex, r, fields)
        minList = [posMin] + self.__getValueAtIndex(ds, minIndex, r, fields)
        return (maxList, minList)
    
    # Public
    def FindOtherFieldsAtExtremaOfMainFeildTS(
        self, numMain, numStart, numStop, rMin=0, r=8,
        chkFile=False, forcedPlot=False, mainField="density", otherFields=[]):
    
        # Read hdf5 file
        dsMain = self.__readFile(numMain, chkFile, forcedPlot)
        
        #  Find the index of extrema
        (maxIndex, minIndex) = self.__findExtremaIndex(dsMain, rMin, r, mainField)

        # Extract the field value time series at the extrema index
        fields = [mainField] + otherFields
        maxValueTimeSeries = [self.__getPosAtIndex(dsMain, maxIndex, r)]
        minValueTimeSeries = [self.__getPosAtIndex(dsMain, minIndex, r)]
        for i in range(numStart, numStop+1):
            ds = self.__readFile(i, chkFile, forcedPlot)
            maxValueTimeSeries.append(self.__getValueAtIndex(ds, maxIndex, r, fields))
            minValueTimeSeries.append(self.__getValueAtIndex(ds, minIndex, r, fields))
        return (maxValueTimeSeries, minValueTimeSeries)

    # Public
    def FindSurroundingOfExtrema(
        self, num, padding, r=8, chkFile=False, forcedPlot=False,
        mainField="density"
    ):
        
        ds = self.__readFile(num, chkFile, forcedPlot)
        fields = [mainField]

        (maxIndex, minIndex) = self.__findExtremaIndex(ds, r, mainField)

        extremaList = []
        for extremaIndex in [minIndex, maxIndex]:
            extremaList.append(self.__getPosAtIndex(ds, extremaIndex, r))
            for i in range(extremaIndex[0] - padding, extremaIndex[0] + padding + 1):
                for j in range(extremaIndex[1] - padding, extremaIndex[1] + padding + 1):
                    for k in range(extremaIndex[2] - padding, extremaIndex[2] + padding + 1):

                        extremaList.append([
                            # getPosAtIndex(ds, (i,j,k), r), 
                            self.__getValueAtIndex(ds, (i, j, k), r, fields)
                        ])
        return extremaList
    

