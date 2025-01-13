from enum import IntEnum
import torch
import os, sys
from common.Log import DebugPrint
import numpy as np


class eSRResNet(IntEnum):
    NONE = 0
    DATA = 1
    WIDTH = 2
    HEIGHT = 3
    IMAGE = 4

class CSRResNet():
    def __init__(self):
        self.__uWidth = 128
        self.__uHeight = 128
        self.__strDevice = "cuda" if torch.cuda.is_available() else "cpu"

    def __del__(self):
        self.Close()

    def Open(self) -> bool:
        strCkptPath = "./super_resolution/checkpoints/checkpoint_srresnet_voxel_x4_" + self.__strDataName +  "_" + str(int(self.__uWidth)) + "x" + str(int(self.__uHeight)) + ".pth.tar"
        if(not os.path.exists(strCkptPath)):
            DebugPrint().error("Checkpoint file does not exist!: " + strCkptPath)
            return False
        DebugPrint().info("Loading SRResNet from %s" % strCkptPath)
        sys.path.insert(0, "./super_resolution")
        self.__oSrResNet = torch.load(strCkptPath)['model'].to(self.__strDevice)
        self.__oSrResNet.eval()
        return True

    def Close(self) -> bool:
        return True
    
    def Control(self, eInformation:int, Value=None) -> bool:
        eInfo = eSRResNet(eInformation)
        if(eInfo == eSRResNet.NONE):
            pass
        elif(eInfo == eSRResNet.DATA):
            self.__strDataName = str(Value)
        elif(eInfo == eSRResNet.WIDTH):
            self.__uWidth = int(Value)
        elif(eInfo == eSRResNet.HEIGHT):
            self.__uHeight = int(Value)
        elif(eInfo == eSRResNet.IMAGE):
            if(type(Value) == np.ndarray):
                self.__oImage = np.array(Value)
                self.__oImage = np.transpose(self.__oImage, (2, 0, 1))
                self.__oImage = np.expand_dims(self.__oImage, axis=0)
                self.__oImage = torch.from_numpy(self.__oImage).float().to(self.__strDevice)
            else:
                self.__oImage = torch.permute(Value, (2, 0, 1))
                self.__oImage = torch.unsqueeze(self.__oImage, 0).to(self.__strDevice)

    def Read(self) -> np.array:
        oInputImg = self.__oImage
        oSrImage = self.__oSrResNet(oInputImg)
        oReturnImg = oSrImage[0].detach().cpu().numpy().transpose(1, 2, 0) * 255
        return oReturnImg
    
    def Reset(self) -> bool:
        return True