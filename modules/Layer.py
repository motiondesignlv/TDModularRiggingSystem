#-*- coding:utf-8 -*-
import maya.cmds as cmds

#コントローラーの階層化
class TDCtlLayering():
    def setAllCtlLayering(self,AllCtlList):
        "【オール】"
        cmds.parent(AllCtlList,"Ctl_GP")

    def setRootCtlLayering(self,RootCtlList):
        "【ルート】"
        cmds.parent(RootCtlList[0],"All_Ctl")
        cmds.parent(RootCtlList[1],"Joint_GP")

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
        cmds.parent(LArmCtlList[0],"IKSystem_GP")
        cmds.parent(RArmCtlList[0],"IKSystem_GP")
        cmds.parent(LArmCtlList[1],"All_Ctl")
        cmds.parent(RArmCtlList[1],"All_Ctl")

        print "result setup.",

    def setFootCtlLayering(self,RFootCtlList,LFootCtlList,RootCtlList):
        "【脚】"
        cmds.parent(RFootCtlList[0],"All_Ctl")
        cmds.parent(LFootCtlList[0],"All_Ctl")
        cmds.parent(RFootCtlList[1],RootCtlList[-1])
        cmds.parent(LFootCtlList[1],RootCtlList[-1])
        cmds.parent(RFootCtlList[2],"IKSystem_GP")
        cmds.parent(LFootCtlList[2],"IKSystem_GP")
        cmds.parent(RFootCtlList[3],"FKIKSystem_GP")
        cmds.parent(LFootCtlList[3],"FKIKSystem_GP")
        cmds.parent(RFootCtlList[4],"IKSystem_GP")
        cmds.parent(LFootCtlList[4],"IKSystem_GP")

    def setSpineCtlLayering(self,SpineCtlList):
        "【ルート】"
        cmds.parent(SpineCtlList[0],"All_Ctl")
        cmds.parent(SpineCtlList[1],"Add_Hips")

    #コントローラーの親子構造を作成
    def setSpineCtlParent(self,RootCtlList,SpineCtlList):
        "Neck → Head"
        #cmds.parentConstraint(NeckCtlList[1],HeadCtlList[1],mo=True)
        "Root → Spine"
        cmds.parentConstraint(RootCtlList,SpineCtlList,mo=True)

    def setNeckCtlParent(self,SpineCtlList,NeckCtlList):
        "Spine → Neck"
        cmds.parentConstraint(SpineCtlList,NeckCtlList,mo=True)
