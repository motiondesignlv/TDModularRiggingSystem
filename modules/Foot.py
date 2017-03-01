#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System

#足のリギング　【LR : 1=左、2=右】,【CtlColor : コントローラーの色】
class TDFootRigging():
    def __init__(self):
        #super(TDFootRigging,self).__init__()
        self.System  = System.ModularRiggingSystem()

    #足リグ用の新しいジョイントを作成
    def createFootJoint(self,footJoints):
        self.footJoint = self.System.createRiggingJoint(footJoints,1,"Add")
        cmds.setAttr(self.footJoint[1]+".preferredAngleX",90)

        return self.footJoint

    #FKジョイントを作成
    def createFootFKJoint(self,footJoints):
        self.FKJoint = self.System.createRiggingJoint(footJoints,0,"FK")#FKジョイントを取得
        cmds.setAttr(self.FKJoint[1]+".preferredAngleX",90)
        self.FKFootGP = self.System.createGP(self.FKJoint[0],"%s_Grp"%self.FKJoint[2])
        #cmds.setAttr(self.FKFootGP+".visibility",0)

        return self.FKJoint

    #IKジョイントを作成
    def createFootIKJoint(self,footJoints):
        self.IKJoint = self.System.createRiggingJoint(footJoints,0,"IK")#FKジョイントを取得
        cmds.setAttr(self.IKJoint[1]+".preferredAngleX",90)
        self.IKFootGP = self.System.createGP(self.IKJoint[0],"%s_Grp"%self.IKJoint[2])
        #cmds.setAttr(self.IKFootGP+".visibility",0)

        return self.IKJoint

    #FK制御用のコントローラーの作成
    def createFootFKCtl(self,FKJoint,CtlColor,CtlScale):
        self.FKFootCtls = [] #FKコントローラーのリスト
        self.FKFootCtlOffset = [] #FKコントローラーのオフセットリスト
        for fkFootCtls in range(len(FKJoint)):
            self.FKFootCtl = self.System.createRigController(self.System.TDcrc.TDCircle,FKJoint[fkFootCtls],FKJoint[fkFootCtls],CtlColor,15*CtlScale)
            if fkFootCtls > 0:
                cmds.parent(self.FKFootCtl[0],self.FKFootCtls[fkFootCtls-1])
            self.FKFootCtls.append(self.FKFootCtl[1])
            self.FKFootCtlOffset.append(self.FKFootCtl[0])
        self.FKFootCtlGP = self.System.createGP(self.FKFootCtlOffset[0],"%s_Grp"%self.FKFootCtls[0])

        return [self.FKFootCtlGP, self.FKFootCtls[-1]]

    #IK制御用のコントローラーを作成
    def createFootIKCtl(self,IKjoint,CtlColor,CtlScale):
        self.IKFootCtr = self.System.TDcrc.TDSquare("%s_Ctl"%IKjoint)
        cmds.setAttr(self.IKFootCtr+".overrideEnabled",1)
        cmds.setAttr(self.IKFootCtr+".overrideColor",CtlColor)
        self.System.setNurbsCtlScaling(self.IKFootCtr,10*CtlScale,15*CtlScale,15*CtlScale)
        self.IKFootCtrOffset = self.System.createGP(self.IKFootCtr,"%s_offset"%self.IKFootCtr)
        self.ctlPosition = cmds.xform(IKjoint,q=True,ws=True,t=True)
        cmds.setAttr(self.IKFootCtrOffset+".translate",self.ctlPosition[0],0,self.ctlPosition[2])
        self.getFootPivot = cmds.xform(IKjoint,q=True,ws=True,rp=True)
        cmds.xform(self.IKFootCtr,ws=True,piv=self.getFootPivot)

        return self.IKFootCtr

    #IKハンドルの作成
    def createFootIKHandle(self,startJoint,endJoint):
        self.footIKHandle = cmds.ikHandle(sj = startJoint,ee = endJoint,
                                sol="ikRPsolver",s="sticky",name="%s_ikHandle"%endJoint)
        self.footIKNull = self.System.createGP(self.footIKHandle[0],"ConnectionFrom__%s"%self.IKFootCtr)
        self.footIKGP = self.System.createGP(self.footIKNull,"%s_IKHandle_Grp"%endJoint)
        cmds.xform(self.footIKGP,piv=[0,0,0])

        return self.footIKGP

    #IKの膝のコントローラー
    def createKneeIKCtl(self,IKjoint,CtlColor,CtlScale):
        self.IKKneeCtl = self.System.createRigController(self.System.TDcrc.TDsphere,IKjoint,IKjoint,CtlColor,1*CtlScale)
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
        cmds.setAttr(self.annotate+"Shape.overrideEnabled",1)
        cmds.setAttr(self.annotate+"Shape.overrideDisplayType",2)
        cmds.setAttr(self.annotateNull[0]+".visibility",0)
        cmds.pointConstraint(self.IKKneeCtl[1],self.annotateNull)
        cmds.parentConstraint(footJoints,self.annotate)

    #IKFKスイッチコントローラーを作成
    def createFootFKIKSwitchCtl(self,footJoints,CtlScale):
        self.FootFKIKSwitchCtl = self.System.createRigController(self.System.TDcrc.TDCross,"%sFKIKSwitch"%footJoints[-1],self.FKJoint[0],20,1*CtlScale)
        self.getPosition = cmds.xform(self.FKJoint[0],q=True,ws=True,rp=True)
        cmds.setAttr(self.FootFKIKSwitchCtl[0]+".rotateX",90)
        cmds.setAttr(self.FootFKIKSwitchCtl[0]+".translateX",self.getPosition[0]*3)
        cmds.pointConstraint(self.footJoint[0],self.FootFKIKSwitchCtl[1],mo=True)

        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"t",1,0)
        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"r",1,0)
        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"s",1,0)
        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"v",1,0)

    #IKFKスイッチコントローラーにFootアトリビュートを追加
    def addFootFKIKSwitchAttr(self,footJoints):
        "Foot"
        cmds.addAttr(self.FootFKIKSwitchCtl[1],ln="Foot",at="enum",en="FK:FK_IK:IK:")
        cmds.setAttr(self.FootFKIKSwitchCtl[1]+".Foot",k=True)
        self.FootSwitch = self.System.createStringAddAttr(self.FootFKIKSwitchCtl[1],"FK_IK","float","FK:IK:",1)
        self.FootSwitchCon1 = cmds.shadingNode("condition",asUtility=True,n="%sCondition1"%self.FootFKIKSwitchCtl[1])
        self.FootSwitchCon2 = cmds.shadingNode("condition",asUtility=True,n="%sCondition2"%self.FootFKIKSwitchCtl[1])
        cmds.connectAttr(self.FootSwitch,self.FootSwitchCon1+".firstTerm")
        cmds.connectAttr(self.FootSwitch,self.FootSwitchCon2+".firstTerm")
        cmds.connectAttr(self.FootSwitchCon1+".outColorR",self.FootSwitchCon2+".colorIfFalseR")
        cmds.connectAttr(self.FootSwitchCon2+".outColorR",self.FootFKIKSwitchCtl[1]+".Foot")
        cmds.setAttr(self.FootSwitchCon2+".secondTerm",1)
        cmds.setAttr(self.FootSwitchCon2+".colorIfTrueR",2)

        return self.FootSwitch

    #Addジョイントへのコンストレイント関係
    def createFootAddJointConnection(self,footJoints):
        self.FKBlendCList = []
        self.IKBlendCList = []
        for Joints in range(len(footJoints)):
            self.FKBlendC = cmds.orientConstraint(self.FKJoint[Joints],self.footJoint[Joints],mo=True,w=0)
            self.IKBlendC = cmds.orientConstraint(self.IKJoint[Joints],self.footJoint[Joints],mo=True,w=1)
            self.FKBlendCList.append(self.FKBlendC[0]+"."+self.FKJoint[Joints]+"W0")
            self.IKBlendCList.append(self.IKBlendC[0]+"."+self.IKJoint[Joints]+"W1")

    #FKコントローラーのコンストレイント関係
    def createFootFKConnection(self,footJoints):
        for Joints in range(len(footJoints)):
            self.System.matrixConstraint(self.FKFootCtls[Joints],self.FKJoint[Joints])

    #IKコントローラーのコンストレイント関係
    def createFootIKConnection(self,footJoints):
        self.IKfootCtrpp = cmds.pointConstraint(self.IKFootCtr,self.footIKNull)
        self.IKfootCtrop = cmds.orientConstraint(self.IKFootCtr,self.IKJoint[2],mo=True)
        #極ベクトルの設定
        cmds.poleVectorConstraint(self.IKKneeCtl[1],self.footIKHandle[0])

    #FKIKスイッチコントローラーのコンストレイント関係
    def createFootFKIKSwitchConnection(self,footJoints):
        #コントローラーのVisibility
        self.reverse = cmds.shadingNode("reverse",asUtility=True,n="%sFKIKReverse"%footJoints[-1])
        self.IKcondition = cmds.shadingNode("condition",asUtility=True,n="%sIKcondition1"%footJoints[-1])
        self.FKcondition = cmds.shadingNode("condition",asUtility=True,n="%sFKcondition2"%footJoints[-1])
        cmds.connectAttr(self.FootSwitch,self.IKcondition+".firstTerm")
        cmds.connectAttr(self.FootSwitch,self.FKcondition+".firstTerm")
        cmds.setAttr(self.FKcondition+".secondTerm",1)
        cmds.connectAttr(self.FKcondition+".outColorR", self.FKFootCtlGP+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", self.footIKCtlGP+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", self.footIKGP+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", self.annotateGrp+".visibility")
        #コンストレイントのウエイト値
        cmds.connectAttr(self.FootSwitch, self.reverse+".inputX")
        for FKBlendCLists in self.FKBlendCList:
            cmds.connectAttr(self.reverse+".outputX",FKBlendCLists)
        for IKBlendCLists in self.IKBlendCList:
            cmds.connectAttr(self.FootSwitch,IKBlendCLists)


    #足リグの階層分け
    def setFootRigLayering(self,footJoints):
        self.footIKCtlGP = cmds.group(self.IKFootCtrOffset,self.IKKneeCtl[0],name="%s_Ctl_Grp"%footJoints)
        cmds.xform(self.footIKCtlGP,piv=[0,0,0])
        self.footIKJointGP = cmds.group(self.footJoint[0],self.IKFootGP,self.FKFootGP,name="%s_Joint_Grp"%footJoints.split("_")[1])
        cmds.xform(self.footIKJointGP,piv=[0,0,0])
        cmds.setAttr(self.footIKJointGP+".visibility",0)
        self.annotateGrp = cmds.group(self.annotate,self.annotateNull,name="%sAnnotate_Grp"%footJoints)
        cmds.xform(self.annotateGrp,piv=[0,0,0])
        self.footCtlGP = cmds.group(self.footIKCtlGP,self.FKFootCtlGP,name="%s_Ctl_Grp"%self.footJoint[-1].split("Add_")[1])
        cmds.xform(self.footCtlGP,piv=[0,0,0])
        self.footFKIKSwitchCtlGP = cmds.group(self.FootFKIKSwitchCtl[0],name="%sFKIKSwitch_Ctl_Grp"%self.footJoint[-1].split("Add_")[1])
        cmds.xform(self.footFKIKSwitchCtlGP,piv=[0,0,0])

        return [self.footCtlGP, self.footIKJointGP,self.annotateGrp,self.footFKIKSwitchCtlGP]
