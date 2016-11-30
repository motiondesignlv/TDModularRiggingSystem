##-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#足のリギング　【LR : 1=左、2=右】,【CtlColor : コントローラーの色】
class TDFootRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setFootRigging(self,footJoints,CtlColor):#LR,CtlColor
        TDFootRigging.createFootJoint(self,footJoints)
        TDFootRigging.createFootFKJoint(self,footJoints)
        self.IKJoint = TDFootRigging.createFootIKJoint(self,footJoints)
        TDFootRigging.createFootIKCtl(self,self.IKJoint[-1],CtlColor)
        self.IKHandleGP = TDFootRigging.createFootIKHandle(self,self.IKJoint[0],self.IKJoint[-1])
        TDFootRigging.createKneeIKCtl(self,self.IKJoint[1],CtlColor)
        TDFootRigging.createAnnotateNode(self,self.IKJoint[1])
        TDFootRigging.createFootConnection(self,footJoints)
        self.IKFootGrpList = TDFootRigging.setFootRigLayering(self,self.IKJoint[-1])

        return [self.IKFootGrpList[0],self.IKFootGrpList[1],self.IKFootGrpList[2],self.IKHandleGP]


    #足リグ用の新しいジョイントを作成
    def createFootJoint(self,footJoints):
        self.footJoint = self.TDMRS.createRiggingJoint(footJoints,1,"Add")
        cmds.setAttr(self.footJoint[1]+".preferredAngleX",90)

        return self.footJoint

    #FKジョイントを作成
    def createFootFKJoint(self,footJoints):
        self.FKJoint = self.TDMRS.createRiggingJoint(footJoints,0,"FK")#FKジョイントを取得
        cmds.setAttr(self.FKJoint[1]+".preferredAngleX",90)
        self.FKFootGP = self.TDMRS.createGP(self.FKJoint[0],"%s_GP"%self.FKJoint[2])
        #cmds.setAttr(self.FKFootGP+".visibility",0)

        return self.FKJoint

    #IKジョイントを作成
    def createFootIKJoint(self,footJoints):
        self.IKJoint = self.TDMRS.createRiggingJoint(footJoints,0,"IK")#FKジョイントを取得
        cmds.setAttr(self.IKJoint[1]+".preferredAngleX",90)
        self.IKFootGP = self.TDMRS.createGP(self.IKJoint[0],"%s_GP"%self.IKJoint[2])
        #cmds.setAttr(self.IKFootGP+".visibility",0)

        return self.IKJoint

    #IK制御用のコントローラーを作成
    def createFootIKCtl(self,IKjoint,CtlColor):
        self.IKFootCtr = self.TDMRS.TDcrc.TDSquare("%s_Ctl"%IKjoint)
        cmds.setAttr(self.IKFootCtr+".overrideEnabled",1)
        cmds.setAttr(self.IKFootCtr+".overrideColor",CtlColor)
        self.TDMRS.setNurbsCtlScaling(self.IKFootCtr,10,15,15)
        self.IKFootCtrOffset = self.TDMRS.createGP(self.IKFootCtr,"%s_offset"%self.IKFootCtr)
        self.ctlPosition = cmds.xform(IKjoint,q=True,ws=True,t=True)
        cmds.setAttr(self.IKFootCtrOffset+".translate",self.ctlPosition[0],0,self.ctlPosition[2])
        self.getFootPivot = cmds.xform(IKjoint,q=True,ws=True,rp=True)
        cmds.xform(self.IKFootCtr,ws=True,piv=self.getFootPivot)

        return self.IKFootCtr

    #IKハンドルの作成
    def createFootIKHandle(self,startJoint,endJoint):
        self.footIKHandle = cmds.ikHandle(sj = startJoint,ee = endJoint,
                                sol="ikRPsolver",s="sticky",name="%s_ikHandle"%endJoint)
        self.footIKNull = self.TDMRS.createGP(self.footIKHandle[0],"ConnectionFrom__%s"%self.IKFootCtr)
        self.footIKGP = self.TDMRS.createGP(self.footIKNull,"%s_IKHandleGrp"%endJoint)
        cmds.xform(self.footIKGP,piv=[0,0,0])

        return self.footIKGP

    #IKの膝のコントローラー
    def createKneeIKCtl(self,IKjoint,CtlColor):
        self.IKKneeCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDsphere,IKjoint,IKjoint,CtlColor,1)
        self.getPivot = cmds.xform(IKjoint,q=True,ws=True,rp=True)
        cmds.xform(self.IKKneeCtl,ws=True,piv = self.getPivot)
        cmds.setAttr(self.IKKneeCtl[0]+".translateZ",self.getPivot[1])

        return self.IKKneeCtl

    #IKの膝のコントローラーの注釈を作成
    def createAnnotateNode(self,footJoints):
        self.getPosition = cmds.xform(footJoints,q=True,ws=True,t=True)
        self.annotateNull = cmds.spaceLocator(n="%s_annotateNull"%footJoints)
        cmds.xform(self.annotateNull,t=self.getPosition)
        self.annotate = cmds.annotate(self.annotateNull)
        self.annotate = cmds.rename(cmds.listRelatives(self.annotate,p=True),"%s_annotate"%footJoints)
        cmds.pointConstraint(self.IKKneeCtl[1],self.annotate)
        cmds.parentConstraint(footJoints,self.annotateNull)

    #コントローラーのコンストレイント関係
    def createFootConnection(self,footJoints):
        for Joints in range(len(footJoints)):
            cmds.orientConstraint(self.FKJoint[Joints],self.footJoint[Joints],mo=True,w=0)
            cmds.orientConstraint(self.IKJoint[Joints],self.footJoint[Joints],mo=True,w=1)
        self.IKfootCtrpp = cmds.pointConstraint(self.IKFootCtr,self.footIKNull)
        self.IKfootCtrop = cmds.orientConstraint(self.IKFootCtr,self.IKJoint[2],mo=True)
        #極ベクトルの設定
        cmds.poleVectorConstraint(self.IKKneeCtl[1],self.footIKHandle[0])

    #足リグの階層分け
    def setFootRigLayering(self,footJoints):
        self.footCtlGP = cmds.group(self.IKFootCtrOffset,self.IKKneeCtl[0],name="%s_Ctl_Grp"%footJoints)
        self.footJointGP = cmds.group(self.footJoint[0],self.IKFootGP,self.FKFootGP,name="%s_Joint_Grp"%footJoints.split("_")[1])
        self.annotateGrp = cmds.group(self.annotate,self.annotateNull,name="%sAnnotate_Grp"%footJoints)
        cmds.xform(self.annotateGrp,piv=[0,0,0])
        cmds.xform(self.footCtlGP,piv=[0,0,0])
        cmds.xform(self.footJointGP,piv=[0,0,0])
        cmds.setAttr(self.footJointGP+".visibility",0)

        return [self.footCtlGP, self.footJointGP,self.annotateGrp]
