#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#スイッチコントローラーのリギング
class TDSwitchCtlRigging():
    def __init__(self):
        self.System  = System.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setSwitchRigging(self,CtlColor):
        self.SwitchCtlList = TDSwitchCtlRigging.createSwitchCtl(self,CtlColor)
        self.ArmAttrList = TDSwitchCtlRigging.createArmSwitchAttr(self)

        return [self.SwitchCtlList, self.ArmAttrList[0], self.ArmAttrList[1]]

    #スイッチコントローラー
    def createSwitchCtl(self,CtlColor):
        self.loc = cmds.spaceLocator(n="All")
        self.SwitchCtl = self.System.createRigController(self.System.TDcrc.TDdial1,"Switch",self.loc,CtlColor,3)
        cmds.delete(self.loc)
        cmds.setAttr(self.SwitchCtl+".rotateX",-90)
        cmds.makeIdentity(self.SwitchCtl,apply=True,t=1,r=1,s=1)
        self.getPivot = cmds.xform(self.System.getJointLabelType()[0,1],q=True,ws=True,rp=True)
        cmds.xform(self.SwitchCtl,ws=True,piv = self.getPivot)
        cmds.setAttr(self.SwitchCtl+".rotateZ",-180)
        cmds.makeIdentity(self.SwitchCtl,apply=True,t=1,r=1,s=1)
        cmds.xform(self.SwitchCtl,cp=True)
        self.System.createHideAttr(self.SwitchCtl,"t",1,0)
        self.System.createHideAttr(self.SwitchCtl,"r",1,0)
        self.System.createHideAttr(self.SwitchCtl,"s",1,0)
        self.System.createHideAttr(self.SwitchCtl,"v",1,0)

        return self.SwitchCtl

    #スイッチコントローラーにArmアトリビュートを追加
    def createArmSwitchAttr(self):
        "Arm"
        cmds.addAttr(self.SwitchCtl,ln="Arm",at="enum",en="FK:FK_IK:IK:")
        cmds.setAttr(self.SwitchCtl+".Arm",k=True)
        self.LeftArmSwitch  = self.System.createStringAddAttr(self.SwitchCtl,"LeftArm_IK_FK","enum","FK:IK:",1)
        self.RightArmSwitch = self.System.createStringAddAttr(self.SwitchCtl,"RightArm_IK_FK","enum","FK:IK:",1)
        self.ArmPMA = cmds.shadingNode("plusMinusAverage",asUtility=True)
        self.ArmMult = cmds.shadingNode("multiplyDivide",asUtility=True)
        cmds.connectAttr(self.LeftArmSwitch,self.ArmPMA+".input1D[0]")
        cmds.connectAttr(self.RightArmSwitch,self.ArmPMA+".input1D[1]")
        cmds.connectAttr(self.ArmPMA+".output1D",self.ArmMult+".input1X")
        cmds.connectAttr(self.ArmMult+".outputX",self.SwitchCtl+".Arm")

        return [self.LeftArmSwitch, self.RightArmSwitch]
