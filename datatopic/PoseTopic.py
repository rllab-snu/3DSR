from dataclasses import dataclass
import numpy as np

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class PixelPose():
    def __init__(self):
        self.__uX_Pix:int = 0
        self.__uY_Pix:int = 0

    @property
    def X_Pix(self) -> int:
        return self.__uX_Pix
    
    @X_Pix.setter
    def X_Pix(self, Data:int) -> None:
        self.__uX_Pix = Data

    @property
    def Y_Pix(self) -> int:
        return self.__uY_Pix
    
    @Y_Pix.setter
    def Y_Pix(self, Data:int) -> None:
        self.__uY_Pix = Data
        
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class PoseData():
    def __init__(self):
        self.__mRotMat:np.ndarray = np.identity(3)
        self.__vTrans:np.ndarray = np.zeros(3)
    
    @property
    def RotationMatrix(self) -> np.ndarray:
        return self.__mRotMat
    
    @RotationMatrix.setter
    def RotationMatrix(self, Data:np.ndarray) -> None:
        self.__mRotMat = Data

    @property
    def Translation(self) -> np.ndarray:
        return self.__vTrans
    
    @Translation.setter
    def Translation(self, Data:np.ndarray) -> None:
        self.__vTrans = Data