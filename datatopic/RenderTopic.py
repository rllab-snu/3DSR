from dataclasses import dataclass
import numpy as np
from datatopic.PoseTopic import PoseData

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class RenderData():
    def __init__(self, Width:np.uint16 = 1200, Height:np.uint16 = 680):
        self.__oRgbImg:np.ndarray = np.zeros((1, Height, Width, 3), dtype=np.uint8)
        self.__oSrcImg:np.ndarray = np.zeros((1, Height, Width, 3), dtype=np.uint8)
        self.__oDepthImg:np.ndarray = np.zeros((1, Height, Width), dtype=np.float32)
        self.__oPose = PoseData()
        self.__oPoseMatrix = np.identity(4)

    @property
    def RgbImg(self):
        return self.__oRgbImg
    
    @RgbImg.setter
    def RgbImg(self, Data) -> None:
        self.__oRgbImg = Data

    @property
    def SrcImg(self) -> np.ndarray:
        return self.__oSrcImg
    
    @SrcImg.setter
    def SrcImg(self, Data:np.ndarray) -> None:
        self.__oSrcImg = Data

    @property
    def DepthImg(self) -> np.ndarray:
        return self.__oDepthImg
    
    @DepthImg.setter
    def DepthImg(self, Data:np.ndarray) -> None:
        self.__oDepthImg = Data

    @property
    def Width(self) -> np.uint16:
        return self.__oRgbImg.shape[2]
    
    @property   
    def Height(self) -> np.uint16:
        return self.__oRgbImg.shape[1]
    
    @property
    def PoseMatrix(self):
        return self.__oPoseMatrix
    
    @PoseMatrix.setter
    def PoseMatrix(self, Data) -> None:
        self.__oPoseMatrix = Data

    @property
    def Pose(self) -> np.ndarray:
        return self.__oPose
    
    @Pose.setter
    def Pose(self, Data:PoseData) -> None:
        self.__oPose = Data   