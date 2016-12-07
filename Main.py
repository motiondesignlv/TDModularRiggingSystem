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

    def build(self):
        self.System.createRigHierarchy()
        self.AllCtlList    = self.All.setAllRigging(20,self.CtlScale)
        self.RootCtlList   = self.Root.setRootRigging(self.System.getJointLabelType()[0,1],14,self.CtlScale)
        #self.SwitchCtlList = self.Switch.setSwitchRigging(20)
        self.SpineCtlList  = self.Spine.setSpineRigging(self.System.getSpineJoint(),17,self.CtlScale)
        self.NeckCtlList   = self.Neck.setNeckRigging(self.System.getNeckJoint(),17,self.CtlScale)
        """
        self.HeadCtlList   = self.Head.setHeadRigging(self.System.getJointLabelType()[0,8],TDMRS.getJointLabelType()[0,7],17)
        """
        self.LFootCtlList  = self.Foot.setFootRigging([self.System.getJointLabelType()[1,2],self.System.getJointLabelType()[1,3],self.System.getJointLabelType()[1,4]],6,self.CtlScale)
        self.RFootCtlList  = self.Foot.setFootRigging([self.System.getJointLabelType()[2,2],self.System.getJointLabelType()[2,3],self.System.getJointLabelType()[2,4]],13,self.CtlScale)

        """
        SwingCtlList  = Swing.setSwingRigging(TDMRS.getJointLabelType()[0,1],4)
        LArmCtlList   = Arm.setArmRigging(1,6,SwitchCtlList[0],SwitchCtlList[1])
        RArmCtlList   = Arm.setArmRigging(2,13,SwitchCtlList[0],SwitchCtlList[2])
        """
        self.Layer.setAllCtlLayering(self.AllCtlList)
        self.Layer.setRootCtlLayering(self.RootCtlList)
        self.Layer.setFootCtlLayering(self.RFootCtlList,self.LFootCtlList,self.RootCtlList)
        print self.RootCtlList
        print self.SpineCtlList
        self.Layer.setCtlParent(self.RootCtlList,self.SpineCtlList)
