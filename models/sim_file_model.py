class SimFileModel:
    simPath: str
    __hdf5FilePrefix: str
    __fileStepMyr: int
    __hdf5FileDigitNum: int = 4
    
    def __init__(self, simPath: str, hdf5FilePrefix: str,
                 fileSterMyr: int, hdf5FileDigitNum: int = 4) -> None:
        self.simPath = simPath
        self.__hdf5FilePrefix = hdf5FilePrefix
        self.__fileStepMyr = fileSterMyr
        self.__hdf5FileDigitNum = hdf5FileDigitNum
    
    
    def getHdf5Path(self, timeMyr):
        return rf"{self.simPath}/{self.__hdf5FilePrefix}_{int(timeMyr/self.__fileStepMyr):0>{self.__hdf5FileDigitNum}d}"
    
    # modeStrMapping = {
        #     Hdf5Mode.PlotFile: "hdf5_plt_cnt",
        #     Hdf5Mode.CheckPointFile: "hdf5_chk",
        #     Hdf5Mode.ForcePlot: "forced_hdf5_plt_cnt"
        # }