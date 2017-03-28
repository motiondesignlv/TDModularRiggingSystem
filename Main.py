# -*- coding: utf-8 -*-

"""モジュラーリギングシステム"""
import maya.cmds as cmds
from TDModularRiggingSystem.lib import Controller
from TDModularRiggingSystem.lib import System
from TDModularRiggingSystem.modules import Arm
from TDModularRiggingSystem.modules import Foot
from TDModularRiggingSystem.modules import Spine
from TDModularRiggingSystem.modules import Neck
from TDModularRiggingSystem.modules import Head
from TDModularRiggingSystem.modules import Root
from TDModularRiggingSystem.modules import Swing
from TDModularRiggingSystem.modules import Switch
from TDModularRiggingSystem.modules import All
from TDModularRiggingSystem.modules import Layer

reload(Controller)
reload(System)
reload(Arm)
reload(Foot)
reload(Spine)
reload(Neck)
reload(Head)
reload(Root)
reload(Swing)
reload(Switch)
reload(All)
reload(Layer)


class SetUP(object):
    def __init__(self):
        self.System  = System.ModularRiggingSystem()
        self.All    = All.TDAllCtlRigging()
        self.Root   = Root.TDRootRigging()
        self.Spine  = Spine.TDSpineRigging()
        self.Neck   = Neck.TDNeckRigging()
        #self.Head   = Head.TDHeadRigging()
        self.Foot   = Foot.TDFootRigging()
        #self.Arm    = Arm.TDArmRigging()
        #self.Swing  = Swing.TDSwingCtlRigging()
        #self.Switch = Switch.TDSwitchCtlRigging()
        self.Layer  = Layer.TDCtlLayering()
        self.CtlScale = 1

    "-----Allリグの構築-----"
    def buildAllRigging(self,CtlColor,CtlScale):
        self.AllCtlList = self.All.createAllCtl(CtlColor,CtlScale)

        return self.AllCtlList

    "-----ルートリグの構築-----"
    def buildRootRigging(self,rootJoints,CtlColor,CtlScale):
        self.rootJoint = self.Root.createRootJoint([rootJoints])
        self.RootCtlList = self.Root.createRootCtl(rootJoints,CtlColor,CtlScale)
        self.Root.createRootCtlConnection()

        return [self.RootCtlList[0],self.RootCtlList[1],self.RootCtlList[2],self.rootJoint[0]]

    "-----背骨リグの構築-----"
    def buildSpineRigging(self,spineJoints,CtlColor,CtlScale):
        #--ジョイントの作成--
        self.SpineJointList = self.Spine.createSpineJoint(spineJoints)
        self.Spine.createSpineFKJoint(spineJoints)
        self.spineIKJoint   = self.Spine.createSpineIKJoint(self.System.getSpineJoint("ik"))
        #--コントローラーの作成--
        self.SpineIKHandleList   = self.Spine.createSpineIKHandle(self.spineIKJoint)
        self.SpineFKCtlList      = self.Spine.createSpineFKCtl(spineJoints,CtlColor,CtlScale)
        self.SpineIKCtlList      = self.Spine.createSpineIKCtl(spineJoints,CtlColor,CtlScale)
        self.SpineFKIKSwitchList = self.Spine.createSpineFKIKSwitchCtl(spineJoints,CtlScale)
        self.Spine.addSpineFKIKSwitchAttr()
        #--コネクション--
        self.Spine.createSpineFKCtlConnection(spineJoints)
        self.Spine.createSpineIKCtlConnection(spineJoints)
        self.Spine.createSpineFKIKSwitchConnection(spineJoints)
        #--階層分け--
        self.SpineParentGrp = self.Spine.createSpineRigConnectParentNull(self.System.getJointLabelType()[0,1])
        self.SpineJointGrp = self.Spine.createSpineRigConnectNull(spineJoints)

        print "--result Spine setup--\n",
        return [self.SpineJointGrp[0],self.SpineJointGrp[1],self.SpineParentGrp]

    "-----首リグの構築-----"
    def buildNeckRigging(self,neckJoints,CtlColor,CtlScale):#,CtlName,parentName
        self.NeckJointList = self.Neck.createNeckJoint(neckJoints)
        self.NeckCtlList = self.Neck.createNeckFKCtl(neckJoints,CtlColor,CtlScale)
        self.Neck.setNeckCtlConnection(self.NeckJointList)
        self.NeckCtlConnectList = self.Neck.createNeckRigConnectNull(self.System.getNeckJoint()[-1])

        return [self.NeckJointList[0],self.NeckCtlList[0],self.NeckCtlList[1],self.NeckCtlConnectList]

    "-----脚リグの構築-----"
    def buildFootRigging(self,footJoints,CtlColor,CtlScale):
        #--ジョイントの作成--
        self.footJoint   = self.Foot.createFootJoint(footJoints)
        self.footFKJoint = self.Foot.createFootJoint(footJoints,"FK")
        self.footIKJoint = self.Foot.createFootJoint(footJoints,"IK")
        #--コントローラーの作成--
        self.footFKCtl         = self.Foot.createFootFKCtl(self.footFKJoint,CtlColor,CtlScale)
        self.footIKCtl         = self.Foot.createFootIKCtl(self.footIKJoint,CtlColor,CtlScale)
        self.footIKHandleGrp   = self.Foot.createFootIKHandle(self.footIKJoint[0],self.footIKJoint[-1],self.footIKCtl)
        self.footKneeIKCtl     = self.Foot.createKneeIKCtl(self.footIKJoint[1],CtlColor,CtlScale)
        self.footAnnotate      = self.Foot.createAnnotateNode(self.footIKJoint[1])
        self.footFKIKSwitchCtl = self.Foot.createFootFKIKSwitchCtl(footJoints,CtlScale)
        self.Foot.addFootFKIKSwitchAttr(self.footFKIKSwitchCtl)
        #--コネクション--
        self.Foot.createFootAddJointConnection(footJoints,self.footJoint,self.footFKJoint,self.footIKJoint)
        self.Foot.createFootFKConnection(footJoints,self.footFKJoint)
        self.Foot.createFootIKConnection(footJoints,self.footIKJoint,self.footIKCtl,self.footKneeIKCtl,self.footIKHandleGrp)
        self.Foot.createFootFKIKSwitchConnection(footJoints,self.footFKCtl,self.footIKCtl,self.footKneeIKCtl,self.footIKHandleGrp,self.footAnnotate)
        #--階層分け--
        #self.IKFootGrpList = self.Foot.setFootRigLayering(self.footIKJoint[-1])

        print "--result Foot setup--\n",
        #return [self.IKFootGrpList[0],self.IKFootGrpList[1],self.IKFootGrpList[2],self.IKFootGrpList[3],self.footIKHandleGrp]


    def build(self,CtlScale=1):
        self.System.createRigHierarchy()
        #self.AllCtlList    = self.buildAllRigging(20,self.CtlScale*CtlScale)
        #self.RootCtlList   = self.buildRootRigging(self.System.getJointLabelType()[0,1],14,self.CtlScale*CtlScale)
        #self.SwitchCtlList = self.Switch.setSwitchRigging(20)
        #self.SpineCtlList  = self.buildSpineRigging(self.System.getSpineJoint("fk"),17,self.CtlScale*CtlScale)
        #self.NeckCtlList   = self.buildNeckRigging(self.System.getNeckJoint(),17,self.CtlScale)
        """
        self.HeadCtlList   = self.Head.setHeadRigging(self.System.getJointLabelType()[0,8],TDMRS.getJointLabelType()[0,7],17)
        """
        self.LFootCtlList  = self.buildFootRigging([self.System.getJointLabelType()[1,2],self.System.getJointLabelType()[1,3],self.System.getJointLabelType()[1,4]],6,self.CtlScale*CtlScale)
        self.RFootCtlList  = self.buildFootRigging([self.System.getJointLabelType()[2,2],self.System.getJointLabelType()[2,3],self.System.getJointLabelType()[2,4]],13,self.CtlScale*CtlScale)

        """
        SwingCtlList  = Swing.setSwingRigging(TDMRS.getJointLabelType()[0,1],4)
        LArmCtlList   = Arm.setArmRigging(1,6,SwitchCtlList[0],SwitchCtlList[1])
        RArmCtlList   = Arm.setArmRigging(2,13,SwitchCtlList[0],SwitchCtlList[2])
        """

        #self.Layer.setAllCtlLayering(self.AllCtlList)
        #self.Layer.setRootCtlLayering(self.RootCtlList)
        #self.Layer.setFootCtlLayering(self.RFootCtlList,self.LFootCtlList,self.RootCtlList)
        #self.Layer.setSpineCtlLayering(self.SpineCtlList,self.RootCtlList,self.SpineFKIKSwitchList,self.SpineIKHandleList)

        #self.Layer.setSpineCtlParent(self.RootCtlList[-1],self.SpineCtlList[-1])
        #self.Layer.setNeckCtlParent(self.SpineCtlList[0],self.NeckCtlList[-1])
