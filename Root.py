#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#ルートのリギング
class TDRootRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setRootRigging(self,rootJoints,CtlColor):
        self.rootJoint = TDRootRigging.createRootJoint(self,[rootJoints])
        self.RootCtlList = TDRootRigging.createRootCtl(self,rootJoints,CtlColor)
        self.createRootCtlConnection(self)

        return [self.RootCtlList[0],self.RootCtlList[1],self.RootCtlList[2],self.rootJoint[0]]

    #ルートリグ用の新しいジョイントを作成
    def createRootJoint(self,rootJoints):
        self.rootJoint = self.TDMRS.createRiggingJoint(rootJoints,1,"Add")

        return self.rootJoint

    #ルートコントローラー
    def createRootCtl(self,rootJoints,CtlColor):
        self.RootCtl = self.TDMRS.createMatrixRigController(self.TDMRS.TDcrc.TDDirFourFat,rootJoints,rootJoints,CtlColor,40)
        self.RootGP = self.TDMRS.createChildAttrToParentGP(self.rootJoint[0],"ConnectionFrom__%s"%self.RootCtl[1])
        self.RootJointGP = self.TDMRS.createGP(self.RootGP,"%sJoint_Offset"%rootJoints)
        self.RootCtlGP = self.TDMRS.createGP(self.RootCtl[0],"%sCtl_Grp"%rootJoints)
        #self.RootCtlOffset = self.TDMRS.createChildAttrToParentGP(self.RootCtl,"%sCtl_Offset"%rootJoints)

        return [self.RootCtlGP,self.RootJointGP,self.RootCtl]

    #ルートコントローラーの関連づけ
    def createRootCtlConnection(self,*argv):
        self.RootCtrpp = self.TDMRS.matrixConstraint(self.RootCtl[1],self.RootGP)

        return self.RootCtrpp
