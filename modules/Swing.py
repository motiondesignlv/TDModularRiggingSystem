#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#スウィングコントローラーのリギング
class TDSwingCtlRigging():
    def __init__(self):
        self.System  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setSwingRigging(self,CtlName,CtlColor):
        self.SwingCtlList = TDSwingCtlRigging.createSwingCtl(self,CtlName,CtlColor)
        TDSwingCtlRigging.createSwingCtlConnection(self,CtlName)

        return self.SwingCtlList

    #腰ふりコントローラー
    def createSwingCtl(self,CtlName,CtlColor):
        self.SwingCtl = self.System.createRigController(self.System.TDcrc.TDDistortCircle,"Swing",CtlName,CtlColor,30)
        self.SwingGP = cmds.group(CtlName,name="Swing_GP")
        self.SwingCtlGP = self.System.createGP(self.SwingCtl,"%s_GP"%self.SwingCtl)

        return [self.SwingCtlGP,self.SwingGP]

    #腰ふりコントローラーの関連づけ
    def createSwingCtlConnection(self,CtlName):
        cmds.xform(self.SwingGP,ws=True,piv = cmds.xform(CtlName,q=True,ws=True,rp=True))
        cmds.connectAttr(self.SwingCtl+".rotate",self.SwingGP+".rotate")
