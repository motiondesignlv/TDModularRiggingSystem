#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#コントローラーの階層化
class TDCtlLayering(System.ModularRiggingSystem):
    def __init__(self):
        System.ModularRiggingSystem.__init__(self)

    def setAllCtlLayering(self,AllCtlList):
        "【オール】"
        cmds.parent(AllCtlList,self.GP2Name[1])

    def setRootCtlLayering(self,RootCtlList):
        "【ルート】"
        cmds.parent(RootCtlList[0],"All_Ctl")
        cmds.parent(RootCtlList[1],self.GP2Name[0])

    def setCtlLayering(self):
        "【スイッチ】"
        cmds.parent(SwitchCtlList[0],"All_Ctl")
        "【ルート】"
        cmds.parent(RootCtlList[2],"All_Ctl")
        cmds.reorder(RootCtlList[0],f=True)
        "【スウィング】"
        cmds.parent(SwingCtlList[0],"All_Ctl")
        #cmds.reorder(self.SwingCtl,f=True)
        "【頭】"
        cmds.parent(NeckCtlList[0],"All_Ctl")
        cmds.parent(HeadCtlList[0],"All_Ctl")
        "【背骨】"
        cmds.parent(SpineCtlList[0],"All_Ctl")
        "【腕】"
        cmds.parent(LArmCtlList[0],self.GP3Name[1])
        cmds.parent(RArmCtlList[0],self.GP3Name[1])
        cmds.parent(LArmCtlList[1],"All_Ctl")
        cmds.parent(RArmCtlList[1],"All_Ctl")

        print "result setup.",

    def setFootCtlLayering(self,RFootCtlList,LFootCtlList,RootCtlList):
        "【脚】"
        cmds.parent(RFootCtlList[0],"All_Ctl")
        cmds.parent(LFootCtlList[0],"All_Ctl")
        cmds.parent(RFootCtlList[1],RootCtlList[-1])
        cmds.parent(LFootCtlList[1],RootCtlList[-1])
        cmds.parent(RFootCtlList[2],self.GP3Name[1])
        cmds.parent(LFootCtlList[2],self.GP3Name[1])
        cmds.parent(RFootCtlList[3],self.GP3Name[2])
        cmds.parent(LFootCtlList[3],self.GP3Name[2])
        cmds.parent(RFootCtlList[4],self.GP3Name[1])
        cmds.parent(LFootCtlList[4],self.GP3Name[1])

    def setSpineCtlLayering(self,SpineCtlList,RootCtlList,SpineFKIKSwitchList,SpineIKHandleList):
        "【背骨】"
        cmds.parent(SpineCtlList[0],"All_Ctl")
        cmds.parent(SpineCtlList[1],RootCtlList[-1])
        cmds.parent(SpineFKIKSwitchList[0],self.GP3Name[2])
        cmds.parent(SpineIKHandleList[0],self.GP3Name[1])


    #コントローラーの親子構造を作成
    def setSpineCtlParent(self,RootCtlList,SpineCtlList):
        "Neck → Head"
        #cmds.parentConstraint(NeckCtlList[1],HeadCtlList[1],mo=True)
        "Root → Spine"
        cmds.parentConstraint(RootCtlList,SpineCtlList,mo=True)

    def setNeckCtlParent(self,SpineCtlList,NeckCtlList):
        "Spine → Neck"
        cmds.parentConstraint(SpineCtlList,NeckCtlList,mo=True)
