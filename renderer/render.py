from enum import IntEnum
from utils.map_viewer import Map_viewer
from common.Log import DebugPrint
from datatopic.RenderTopic import RenderData
from super_resolution.srresnet import *

class eRender(IntEnum):
    NONE = 0
    DATA_PATH = 1
    WIDTH = 2
    HEIGHT = 3
    FOCAL_X = 4
    FOCAL_Y = 5
    CENTER_X = 6
    CENTER_Y = 7
    DATA = 8
    USE_SR = 9

class CRender():
    def __init__(self):
        self.__strDataPath = ''
        self.__uH = 128
        self.__uW = 128
        self.__fFx = self.__uW / 2
        self.__fFy = self.__uH / 2
        self.__fCx = self.__uW / 2 - 0.5
        self.__fCy = self.__uH / 2 - 0.5
        self.__strDataName = ''
        self.__oMapViewer = None
        self.__oSrResNet = CSRResNet()
        self.__bUseSR = True
        
    def __del__(self):
        pass

    def Open(self) -> bool:
        if(self.__strDataPath == '' or self.__strDataName == ''):
            DebugPrint().error("Data path is not set.")
            return False
        DebugPrint().info("Loading data from %s, with W=%d, H=%d, fx=%f, fy=%f, cx=%f, cy=%f" % (self.__strDataPath, self.__uW, self.__uH, self.__fFx, self.__fFy, self.__fCx, self.__fCy))
        
        if(self.__bUseSR): 
            self.__oSrResNet.Control(eSRResNet.DATA, self.__strDataName)
            if(not self.__oSrResNet.Open()):
                DebugPrint().error("Failed to open SRResNet.")
                return False
        self.__oMapViewer = Map_viewer(data_path = self.__strDataPath, H = self.__uH, W = self.__uW, fx = self.__fFx, fy = self.__fFy, cx = self.__fCx, cy = self.__fCy)
        return True
    
    def Close(self) -> bool:
        pass

    def Control(self, eInformation:int, Value=None) -> bool:
        eInfo = eRender(eInformation)
        if(eInfo == eRender.NONE):
            pass
        elif(eInfo == eRender.DATA_PATH):
            self.__strDataPath = str(Value)
        elif(eInfo == eRender.WIDTH):
            self.__uW = int(Value)
            if(self.__bUseSR): self.__oSrResNet.Control(eSRResNet.WIDTH, self.__uW)
        elif(eInfo == eRender.HEIGHT):
            self.__uH = int(Value)
            if(self.__bUseSR): self.__oSrResNet.Control(eSRResNet.HEIGHT, self.__uH)
        elif(eInfo == eRender.FOCAL_X):
            self.__fFx = float(Value)
        elif(eInfo == eRender.FOCAL_Y):
            self.__fFy = float(Value)
        elif(eInfo == eRender.CENTER_X):
            self.__fCx = float(Value)
        elif(eInfo == eRender.CENTER_Y):
            self.__fCy = float(Value)
        elif(eInfo == eRender.DATA):
            self.__strDataName = str(Value)
        elif(eInfo == eRender.USE_SR):
            self.__bUseSR = bool(Value)
        
    def Reset(self) -> bool:
        pass

    def Write(self) -> bool:
        pass

    def Read(self, readoutData:RenderData) -> bool:
        mRenderPose = readoutData.PoseMatrix
        oRenderImg = self.__oMapViewer.render_img(mRenderPose)
        oRenderDepth = self.__oMapViewer.render_depth(mRenderPose)
        if(self.__bUseSR):
            self.__oSrResNet.Control(eSRResNet.IMAGE, oRenderImg)
            oSrImg = self.__oSrResNet.Read()
        else:
            oSrImg = oRenderImg * 255
        readoutData.SrcImg = oRenderImg
        readoutData.RgbImg = oSrImg
        readoutData.DepthImg = oRenderDepth
        return True
    
    def GetPoses(self):
        return self.__oMapViewer.est_poses