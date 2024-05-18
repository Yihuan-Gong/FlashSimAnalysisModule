from  matplotlib.pyplot import Figure
import matplotlib.pyplot as plt
from typing import Callable, List, TypeVar
import cv2
import os

from ..models import Video2dInfoModel
from ....plot.plot2d import Plot2dInfoModel
from .....models.interfaces import DataNdCalculationInfoModel


TcalcInfo = TypeVar("TcalcInfo")

class Video2dMaker:
    
    def makeVideo(
        self,
        calculationInfo: TcalcInfo,
        plotInfo: Plot2dInfoModel,
        videoInfo: Video2dInfoModel,
        plotAction: Callable[[TcalcInfo, Plot2dInfoModel], Figure]
    ):
        if (not isinstance(calculationInfo, DataNdCalculationInfoModel)):
            raise ValueError("calculationInfo should be the instance of DataNdCalculationInfoModel")
        
        # Plot all images
        calcInfoList = videoInfo.getCalcInfoList(calculationInfo)
        for calInfo in calcInfoList:
            plotInfo.ax = None
            plotInfo.fig = None
            frame = plotAction(calInfo, plotInfo)
            frame.savefig(self.__getFigPath(videoInfo.imageDir, calInfo))
            plt.close(frame)
            
        # Initial video writer by the image size of first image
        img = cv2.imread(self.__getFigPath(videoInfo.imageDir, calcInfoList[0]))
        size = (img.shape[1], img.shape[0])  # (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(self.__getVideoPath(videoInfo), fourcc, videoInfo.fps, size)

        # Make the video by all images
        for calcInfo in calcInfoList:
            img = cv2.imread(self.__getFigPath(videoInfo.imageDir, calcInfo))
            video.write(img)

        cv2.destroyAllWindows()
        video.release()
    
        
    def __getFigPath(self, imageDir: str, calcInfo: DataNdCalculationInfoModel):
        imageDir: str = f"{imageDir}/{calcInfo.rBoxKpc}kpc/"
        self.__mkdirIfDne(imageDir)
        return f"{imageDir}/{calcInfo.timeMyr}Myr.png"
    
    
    def __getVideoPath(self, videoInfo: Video2dInfoModel):
        self.__mkdirIfDne(videoInfo.videoDir)
        return f"{videoInfo.videoDir}/{videoInfo.videoName}.mp4"
    
    
    
    def __mkdirIfDne(self, dir: str):
        if (not os.path.exists(dir)):
            os.makedirs(dir)