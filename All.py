#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#Allコントローラーのリギング
class TDAllCtlRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setAllRigging(self,CtlColor):
        self.AllCtlList = TDAllCtlRigging.createAllCtl(self,CtlColor)

        return self.AllCtlList

    #オールコントローラー
    def createAllCtl(self,CtlColor):
        #self.loc = cmds.spaceLocator(n="All")
        self.AllGrp = cmds.group(em=True,n="All")
        self.AllCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDTransform,self.AllGrp,self.AllGrp,CtlColor,30)
        cmds.delete(self.AllGrp)
        self.AllGrp = cmds.group(self.AllCtl[0],n="%s_Grp"%self.AllCtl[1])
        cmds.xform(self.AllGrp,piv=[0,0,0])
        self.TDMRS.createHideAttr("helperArrows_GP","t",1,0)
        self.TDMRS.createHideAttr("helperArrows_GP","r",1,0)
        self.TDMRS.createHideAttr("helperArrows_GP","s",1,0)
        self.TDMRS.createHideAttr("helperArrows_GP","v",1,0)

        return self.AllGrp
