# -*- coding: utf-8 -*-

"""モジュラーリギングシステム"""
import maya.cmds as cmds
from TDModularRiggingSystem import RigController
from TDModularRiggingSystem import RiggingSystem
from TDModularRiggingSystem import Arm
from TDModularRiggingSystem import Foot
from TDModularRiggingSystem import Spine
from TDModularRiggingSystem import Neck
from TDModularRiggingSystem import Head
from TDModularRiggingSystem import Root
from TDModularRiggingSystem import Swing
from TDModularRiggingSystem import Switch
from TDModularRiggingSystem import All

reload(RigController)
reload(RiggingSystem)
reload(Arm)
reload(Foot)
reload(Spine)
reload(Neck)
reload(Head)
reload(Root)
reload(Swing)
reload(Switch)
reload(All)

#コントローラーの階層化
class TDCtlLayering():
    def setCtlLayering(self):
        "【オール】"
        cmds.parent(AllCtlList,"Ctl_GP")
        cmds.parent(RootCtlList[1],"Joint_GP")
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
        "【脚】"
        cmds.parent(RFootCtlList[0],"IKSystem_GP")
        cmds.parent(LFootCtlList[0],"IKSystem_GP")
        cmds.parent(RFootCtlList[1],"All_Ctl")
        cmds.parent(LFootCtlList[1],"All_Ctl")
        cmds.parent(RFootCtlList[2],"JointSystem_GP")
        cmds.parent(LFootCtlList[2],"JointSystem_GP")
        
        print "result setup.",
    
    #コントローラーの親子構造を作成
    def setCtlParent(self):
        "Neck → Head"
        cmds.parentConstraint(NeckCtlList[1],HeadCtlList[1],mo=True)
        "Spine → Neck"
        cmds.parentConstraint(SpineCtlList[1],NeckCtlList[-1],mo=True)
        "Root → Spine"
        cmds.parentConstraint(RootCtlList[0],SpineCtlList[-1],mo=True)
        


TDMRS  = RiggingSystem.ModularRiggingSystem()
All    = All.TDAllCtlRigging()
Root   = Root.TDRootRigging()
Spine  = Spine.TDSpineRigging()
Neck   = Neck.TDHeadRigging()
Head   = Head.TDHeadRigging()
Foot   = Foot.TDFootRigging()
Arm    = Arm.TDArmRigging()
Swing  = Swing.TDSwingCtlRigging()
Switch = Switch.TDSwitchCtlRigging()
Layer  = TDCtlLayering()


TDMRS.createRigHierarchy()
AllCtlList    = All.setAllRigging(20)
RootCtlList   = Root.setRootRigging(TDMRS.getJointLabelType()[0,1],14)
SwitchCtlList = Switch.setSwitchRigging(20)
SpineCtlList  = Spine.setSpineRigging(TDMRS.getJointLabelType()[0,1],17)
NeckCtlList   = Neck.setHeadRigging(TDMRS.getJointLabelType()[0,7],TDMRS.getJointLabelType()[0,6],17)
HeadCtlList   = Head.setHeadRigging(TDMRS.getJointLabelType()[0,8],TDMRS.getJointLabelType()[0,7],17)
LFootCtlList  = Foot.setFootRigging(1,6)
RFootCtlList  = Foot.setFootRigging(2,13)
SwingCtlList  = Swing.setSwingRigging(TDMRS.getJointLabelType()[0,1],4)
LArmCtlList   = Arm.setArmRigging(1,6,SwitchCtlList[0],SwitchCtlList[1])
RArmCtlList   = Arm.setArmRigging(2,13,SwitchCtlList[0],SwitchCtlList[2])
Layer.setCtlLayering()
Layer.setCtlParent()
