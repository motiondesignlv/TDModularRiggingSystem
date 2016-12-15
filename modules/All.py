#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#Allコントローラーのリギング
class TDAllCtlRigging():
    def __init__(self):
        self.System  = System.ModularRiggingSystem()

    """
    "-----コマンドの実行-----"
    def setAllRigging(self,CtlColor,CtlScale):
        self.AllCtlList = TDAllCtlRigging.createAllCtl(self,CtlColor,CtlScale)

        return self.AllCtlList
    """

    #オールコントローラー
    def createAllCtl(self,CtlColor,CtlScale):
        #self.loc = cmds.spaceLocator(n="All")
        self.AllGrp = cmds.group(em=True,n="All")
        self.AllCtl = self.System.createRigController(self.System.TDcrc.TDTransform,self.AllGrp,self.AllGrp,CtlColor,30*CtlScale)
        cmds.delete(self.AllGrp)
        self.AllGrp = cmds.group(self.AllCtl[0],n="%s_Grp"%self.AllCtl[1])
        cmds.xform(self.AllGrp,piv=[0,0,0])
        self.System.createHideAttr("helperArrows_GP","t",1,0)
        self.System.createHideAttr("helperArrows_GP","r",1,0)
        self.System.createHideAttr("helperArrows_GP","s",1,0)
        self.System.createHideAttr("helperArrows_GP","v",1,0)

        return self.AllGrp
