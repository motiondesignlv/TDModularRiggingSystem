#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#ルートのリギング
class TDRootRigging():
    def __init__(self):
        self.System  = System.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setRootRigging(self,rootJoints,CtlColor,CtlScale):
        self.rootJoint = TDRootRigging.createRootJoint(self,[rootJoints])
        self.RootCtlList = TDRootRigging.createRootCtl(self,rootJoints,CtlColor,CtlScale)
        self.createRootCtlConnection(self)

        return [self.RootCtlList[0],self.RootCtlList[1],self.RootCtlList[2],self.rootJoint[0]]

    #ルートリグ用の新しいジョイントを作成
    def createRootJoint(self,rootJoints):
        self.rootJoint = self.System.createRiggingJoint(rootJoints,1,"Add")

        return self.rootJoint

    #ルートコントローラー
    def createRootCtl(self,rootJoints,CtlColor,CtlScale):
        self.RootCtl = self.System.createMatrixRigController(self.System.TDcrc.TDDirFourFat,rootJoints,rootJoints,CtlColor,40*CtlScale)
        self.RootGP = self.System.createChildAttrToParentGP(self.rootJoint[0],"ConnectionFrom__%s"%self.RootCtl[1])
        self.RootJointGP = self.System.createGP(self.RootGP,"%sJoint_Offset"%rootJoints)
        self.RootCtlGP = self.System.createGP(self.RootCtl[0],"%sCtl_Grp"%rootJoints)
        #self.RootCtlOffset = self.System.createChildAttrToParentGP(self.RootCtl,"%sCtl_Offset"%rootJoints)

        return [self.RootCtlGP,self.RootJointGP,self.RootCtl]

    #ルートコントローラーの関連づけ
    def createRootCtlConnection(self,*argv):
        self.RootCtrpp = self.System.matrixConstraint(self.RootCtl[1],self.RootGP)

        return self.RootCtrpp
