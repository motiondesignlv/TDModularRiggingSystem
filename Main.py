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
        self.SpineJointList = self.Spine.createSpineJoint(spineJoints)
        self.Spine.createSpineFKJoint(spineJoints)
        self.SpineCtlList = self.Spine.createSpineFKCtl(spineJoints,CtlColor,CtlScale)
        self.Spine.createSpineFKCtlConnection(spineJoints)
        self.SpineJointGrp = self.Spine.createSpineRigConnectNull(self.System.getJointLabelType()[0,1])

        print "--result Spine setup--\n",
        return [self.SpineJointGrp[0],self.SpineJointGrp[1],self.SpineJointList[-1],self.SpineCtlList[0],self.SpineCtlList[1],self.SpineJointGrp[-1]]

    "-----首リグの構築-----"
    def buildNeckRigging(self,neckJoints,CtlColor,CtlScale):#,CtlName,parentName
        self.NeckJointList = self.Neck.createNeckJoint(neckJoints)
        self.NeckCtlList = self.Neck.createNeckFKCtl(neckJoints,CtlColor,CtlScale)
        self.Neck.setNeckCtlConnection(self.NeckJointList)
        self.NeckCtlConnectList = self.Neck.createNeckRigConnectNull(self.System.getSpineJoint()[-1])

        return [self.NeckJointList[0],self.NeckCtlList[0],self.NeckCtlList[1],self.NeckCtlConnectList]

    "-----脚リグの構築-----"
    def buildFootRigging(self,footJoints,CtlColor,CtlScale):
        #--ジョイントの作成--
        self.Foot.createFootJoint(footJoints)
        self.FKJoint = self.Foot.createFootFKJoint(footJoints)
        self.IKJoint = self.Foot.createFootIKJoint(footJoints)
        #--コントローラーの作成--
        self.Foot.createFootFKCtl(self.FKJoint,CtlColor,CtlScale)
        self.Foot.createFootIKCtl(self.IKJoint[-1],CtlColor,CtlScale)
        self.IKHandleGP = self.Foot.createFootIKHandle(self.IKJoint[0],self.IKJoint[-1])
        self.Foot.createKneeIKCtl(self.IKJoint[1],CtlColor,CtlScale)
        self.Foot.createAnnotateNode(self.IKJoint[1])
        self.Foot.createFootFKIKSwitchCtl(footJoints,CtlScale)
        self.Foot.addFootFKIKSwitchAttr(footJoints)
        #--コントローラーとジョイントのコネクション--
        self.Foot.createFootAddJointConnection(footJoints)
        self.Foot.createFootFKConnection(footJoints)
        self.Foot.createFootIKConnection(footJoints)
        #--コントローラーとジョイントの階層分け--
        self.IKFootGrpList = self.Foot.setFootRigLayering(self.IKJoint[-1])
        self.Foot.createFootFKIKSwitchConnection(footJoints)

        print "--result Foot setup--\n",
        return [self.IKFootGrpList[0],self.IKFootGrpList[1],self.IKFootGrpList[2],self.IKFootGrpList[3],self.IKHandleGP]

    def build(self):
        self.System.createRigHierarchy()
        self.AllCtlList    = self.buildAllRigging(20,self.CtlScale)
        self.RootCtlList   = self.buildRootRigging(self.System.getJointLabelType()[0,1],14,self.CtlScale)
        #self.SwitchCtlList = self.Switch.setSwitchRigging(20)
        self.SpineCtlList  = self.buildSpineRigging(self.System.getSpineJoint(),17,self.CtlScale)
        self.NeckCtlList   = self.buildNeckRigging(self.System.getNeckJoint(),17,self.CtlScale)
        """
        self.HeadCtlList   = self.Head.setHeadRigging(self.System.getJointLabelType()[0,8],TDMRS.getJointLabelType()[0,7],17)
        """
        self.LFootCtlList  = self.buildFootRigging([self.System.getJointLabelType()[1,2],self.System.getJointLabelType()[1,3],self.System.getJointLabelType()[1,4]],6,self.CtlScale)
        self.RFootCtlList  = self.buildFootRigging([self.System.getJointLabelType()[2,2],self.System.getJointLabelType()[2,3],self.System.getJointLabelType()[2,4]],13,self.CtlScale)

        """
        SwingCtlList  = Swing.setSwingRigging(TDMRS.getJointLabelType()[0,1],4)
        LArmCtlList   = Arm.setArmRigging(1,6,SwitchCtlList[0],SwitchCtlList[1])
        RArmCtlList   = Arm.setArmRigging(2,13,SwitchCtlList[0],SwitchCtlList[2])
        """
        self.Layer.setAllCtlLayering(self.AllCtlList)
        self.Layer.setRootCtlLayering(self.RootCtlList)
        self.Layer.setFootCtlLayering(self.RFootCtlList,self.LFootCtlList,self.RootCtlList)
        self.Layer.setSpineCtlLayering(self.SpineCtlList)
        print self.SpineCtlList

        self.Layer.setSpineCtlParent(self.RootCtlList[-1],self.SpineCtlList[-1])
        self.Layer.setNeckCtlParent(self.SpineCtlList[0],self.NeckCtlList[-1])
