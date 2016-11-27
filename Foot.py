#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#足のリギング　【LR : 1=左、2=右】,【CtlColor : コントローラーの色】
class TDFootRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setFootRigging(self,LR,CtlColor):
        TDFootRigging.createFootJoint(self,LR)
        TDFootRigging.createFKFootJoint(self,LR,CtlColor)
        TDFootRigging.createIKFootJoint(self,LR,CtlColor)
        self.IKFootCtlList = TDFootRigging.createIKFootCtl(self,LR,CtlColor)
        self.IKKneeCtlList = TDFootRigging.createIKKneeCtl(self,LR,CtlColor)
        TDFootRigging.createFootConnection(self)
        self.IKFootGrpList = TDFootRigging.setIKFootCtlLayering(self,LR)

        return [self.IKFootCtlList] + self.IKFootGrpList + [self.IKKneeCtlList]

    #足リグ用の新しいジョイントを作成
    def createFootJoint(self,LR):
        self.footJoint = self.TDMRS.createRiggingJoint(self.TDMRS.getBetweenJoint(self.TDMRS.getJointLabelType()[LR,2],self.TDMRS.getJointLabelType()[LR,4]))
        return self.footJoint

    #FKジョイントを作成
    def createFKFootJoint(self,LR,CtlColor):
        self.FKJoint = []#FKジョイントを取得
        cmds.select(d=True)
        for FKJoints in self.footJoint:
            self.FKJ = cmds.joint(r=True,p=self.TDMRS.getJointWPosition(FKJoints),n="FK%s"%FKJoints)
            self.FKJoint.append(self.FKJ)
        self.FKFootGP = self.TDMRS.createGP(self.FKJoint[0],"%s_GP"%self.FKJoint[2])
        cmds.setAttr(self.FKFootGP+".visibility",0)

    #IKジョイントを作成
    def createIKFootJoint(self,LR,CtlColor):
        self.IKJoint = []#FKジョイントを取得
        cmds.select(d=True)
        for IKJoints in self.footJoint:
            self.IKJ = cmds.joint(r=True,p=self.TDMRS.getJointWPosition(IKJoints),n="IK%s"%IKJoints)
            cmds.setAttr(self.IKJ+".preferredAngleX",90)
            self.IKJoint.append(self.IKJ)
        self.IKFootGP = self.TDMRS.createGP(self.IKJoint[0],"%s_GP"%self.IKJoint[2])
        cmds.setAttr(self.IKFootGP+".visibility",0)

    #IKのコントローラーの作成
    def createIKFootCtl(self,LR,CtlColor):
        if LR == 1:self.LeftRight = ["Left"]
        elif LR == 2:self.LeftRight = ["Right"]
        #IKの足のコントローラー
        self.IKFootCtr = self.TDMRS.TDcrc.TDSquare("IK%s_Ctl"%self.TDMRS.getJointLabelType()[LR,4])
        cmds.setAttr(self.IKFootCtr+".overrideEnabled",1)
        cmds.setAttr(self.IKFootCtr+".overrideColor",CtlColor)
        cmds.setAttr(self.IKFootCtr+".scale",10,15,15)
        self.IKFootCtrpp = cmds.pointConstraint(self.TDMRS.gp,self.IKFootCtr,sk="y")
        cmds.delete(self.IKFootCtrpp)
        cmds.setAttr(self.IKFootCtr+".translateZ",15)
        cmds.makeIdentity(self.IKFootCtr,apply=True,t=1,r=1,s=1)
        self.getFootPivot = cmds.xform(self.IKJoint[2],q=True,ws=True,rp=True)
        cmds.xform(self.IKFootCtr,piv=self.getFootPivot)
        self.footIK = cmds.ikHandle(sj = self.IKJoint[0],ee = self.IKJoint[2],
                                sol="ikRPsolver",s="sticky",name="%s_ikHandle"%self.TDMRS.getJointLabelType()[LR,4])
        self.footIKNull = self.TDMRS.createGP(self.footIK[0],"ConnectionFrom__%s"%self.IKFootCtr)
        self.footIKGP = self.TDMRS.createGP(self.footIKNull,"%sIKHandle_GP"%self.LeftRight[0])

        return self.footIKGP

    #IKの膝のコントローラー
    def createIKKneeCtl(self,LR,CtlColor):
        self.IKKneeCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDsphere,"IK"+self.TDMRS.getJointLabelType()[LR,3],self.TDMRS.getJointLabelType()[LR,2],CtlColor,1)
        self.getPivot = cmds.xform(self.IKJoint[1],q=True,ws=True,rp=True)
        cmds.xform(self.IKKneeCtl,ws=True,piv = self.getPivot)
        cmds.setAttr(self.IKKneeCtl+".rotateX",90)
        cmds.makeIdentity(self.IKKneeCtl,apply=True,t=1,r=1,s=1)
        cmds.xform(self.IKKneeCtl,cp=True)

        return self.IKKneeCtl

    #コントローラーのコンストレイント関係
    def createFootConnection(self):
        for Joints in range(len(self.footJoint)):
            cmds.orientConstraint(self.FKJoint[Joints],self.footJoint[Joints],mo=True,w=0)
            cmds.orientConstraint(self.IKJoint[Joints],self.footJoint[Joints],mo=True,w=1)
        self.IKfootCtrpp = cmds.pointConstraint(self.IKFootCtr,self.footIKNull)
        self.IKfootCtrop = cmds.orientConstraint(self.IKFootCtr,self.IKJoint[2],mo=True)
        cmds.poleVectorConstraint(self.IKKneeCtl,self.footIK[0])

    #足のコントローラーの階層分け
    def setIKFootCtlLayering(self,LR):
        if LR == 1:self.LeftRight = ["Left"]
        elif LR == 2:self.LeftRight = ["Right"]
        self.footCtlGP = cmds.group(self.IKFootCtr,self.IKKneeCtl,name="IK%sFootCtl_GP"%self.LeftRight[0])
        self.footJointGP = cmds.group(self.footJoint[0],self.IKFootGP,self.FKFootGP,name="%sFootJoint_GP"%self.LeftRight[0])
        cmds.setAttr(self.footJointGP+".visibility",0)

        return [self.footCtlGP, self.footJointGP]
