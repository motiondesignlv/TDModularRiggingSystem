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
        #TDAllCtlRigging.addAllCtlClass(self)

        return self.AllCtlList

    #オールコントローラー
    def createAllCtl(self,CtlColor):
        self.loc = cmds.spaceLocator(n="All")
        self.AllCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDTransform,self.loc[0],self.loc[0],CtlColor,30)
        cmds.delete(self.loc)
        self.TDMRS.createHideAttr("helperArrows_GP","t",1,0)
        self.TDMRS.createHideAttr("helperArrows_GP","r",1,0)
        self.TDMRS.createHideAttr("helperArrows_GP","s",1,0)
        self.TDMRS.createHideAttr("helperArrows_GP","v",1,0)

        return self.AllCtl

    #足クラスとルートクラスとスイッチクラスにHipコントローラー名を追加
    def addAllCtlClass(self):
        TDFootRigging.AllCtl  = self.AllCtl
        #TDRootRigging.AllCtl  = self.AllCtl
        TDSwitchCtlRigging.AllCtl = self.AllCtl
        TDCtlLayering.AllCtl = self.AllCtl
