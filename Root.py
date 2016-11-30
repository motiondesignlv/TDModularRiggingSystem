#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#ルートのリギング
class TDRootRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setRootRigging(self,CtlName,CtlColor):
        self.RootCtlList = TDRootRigging.createRootCtl(self,CtlName,CtlColor)
        self.createRootCtlConnection(self)

        return self.RootCtlList

    #ルートコントローラー
    def createRootCtl(self,CtlName,CtlColor):
        self.RootCtl = self.TDMRS.createMatrixRigController(self.TDMRS.TDcrc.TDDirFourFat,CtlName,CtlName,CtlColor,40)
        self.RootGP = self.TDMRS.createChildAttrToParentGP(CtlName,"%sConnection_From__%s"%(CtlName,self.RootCtl))
        self.RootCtlGP = self.TDMRS.createGP(self.RootCtl,"%s_GP"%self.RootCtl)
        self.RootCtlOffset = self.TDMRS.createChildAttrToParentGP(self.RootCtl,"%s_Offset"%self.RootCtl)

        return [self.RootCtl,self.RootGP,self.RootCtlGP]

    #ルートコントローラーの関連づけ
    def createRootCtlConnection(self,*argv):
        self.RootCtrpp = self.TDMRS.matrixConstraint(self.RootCtl,self.RootGP)

        return self.RootCtrpp
