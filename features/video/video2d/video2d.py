from .models import Video2dInfoModel
from .utilities import Video2dMaker
from ...plot.plot2d import *


class Video2d:
    
    def velocityFiltering(
        self,
        field: VelocityFilteringField,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: VelocityFilteringCalculationInfoModel,
        plotInfo: Plot2dInfoModel,
        videoInfo: Video2dInfoModel
    ):
        self.__setDefault(
            videoInfo=videoInfo,
            simPath=simFile.simPath,
            spec="velocityFiltering/" + f"{field}".split(".")[-1],
            rKpc=calculationInfo.rBoxKpc
        )
        Video2dMaker().makeVideo(
            calculationInfo=calculationInfo,
            plotInfo=plotInfo,
            videoInfo=videoInfo,
            plotAction=lambda calcInfo, plotInfo: Plot2d().velocityFiltering(
                field=field,
                axis=axis,
                simFile=simFile,
                calculationInfo=calcInfo,
                plotInfo=plotInfo
            )[0]
        )
    
    
    
    def losVelDispersion(
        self,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: LosDispersionCalculationInfoModel,
        plotInfo: Plot2dInfoModel,
        videoInfo: Video2dInfoModel
    ):
        self.__setDefault(
            videoInfo=videoInfo,
            simPath=simFile.simPath,
            spec="losVelDispersion",
            rKpc=calculationInfo.rBoxKpc
        )
        Video2dMaker().makeVideo(
            calculationInfo=calculationInfo,
            plotInfo=plotInfo,
            videoInfo=videoInfo,
            plotAction=lambda calcInfo, plotInfo: Plot2d().losVelDispersion(
                axis=axis,
                simFile=simFile,
                calculationInfo=calcInfo,
                plotInfo=plotInfo
            )[0]
        )
    
    
    def turbulenceHeatingVazza(
        self,
        mode: TurbulenceHeatingVazzaMode,
        axis: str,
        simFile: SimFileModel,
        calculationInfo: TurbulenceHeatingVazzaCalculationInfoModel,
        plotInfo: Plot2dInfoModel,
        videoInfo: Video2dInfoModel
    ):
        self.__setDefault(
            videoInfo=videoInfo,
            simPath=simFile.simPath,
            spec="turbulenceHeatingVazza" + f"{mode}".split(".")[-1],
            rKpc=calculationInfo.rBoxKpc
        )
        Video2dMaker().makeVideo(
            calculationInfo=calculationInfo,
            plotInfo=plotInfo,
            videoInfo=videoInfo,
            plotAction=lambda calcInfo, plotInfo: Plot2d().turbulenceHeatingVazza(
                mode=mode,
                axis=axis,
                simFile=simFile,
                calculationInfo=calcInfo,
                plotInfo=plotInfo
            )[0]
        )
        
    
    def __setDefault(
        self, 
        videoInfo: Video2dInfoModel,
        simPath: str,
        spec: str,
        rKpc: int
    ):
        if (videoInfo.imageDir == "default"):
            videoInfo.imageDir = f"{simPath}/image2d/{spec}/"
        if (videoInfo.videoDir == "default"):
            videoInfo.videoDir = f"{simPath}/video2d/{spec}/"
        if (videoInfo.videoName == "default"):
            videoInfo.videoName = f"{rKpc}kpc"
    

    