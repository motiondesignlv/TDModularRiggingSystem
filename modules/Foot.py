#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System

#足のリギング　【LR : 1=左、2=右】,【CtlColor : コントローラーの色】
class TDFootRigging():
    def __init__(self):
        #super(TDFootRigging,self).__init__()
        self.System  = System.ModularRiggingSystem()

    #足リグ用の新しいジョイントを作成
    def createFootJoint(self,footJoints,type="Add"):
        if type == "Add":
            self.footJoint = self.System.createRiggingJoint(footJoints,1,type)
        else:
            self.footJoint = self.System.createRiggingJoint(footJoints,0,type)
        cmds.setAttr(self.footJoint[1]+".preferredAngleX",90)
        self.footJointGrp = self.System.createCenterPivotGP(self.footJoint[0],"%s_Grp"%self.footJoint[2])
        #cmds.setAttr(self.footJointGrp+".visibility",0)

        return self.footJoint

    #FK制御用のコントローラーの作成
    def createFootFKCtl(self,FKJoint,CtlColor,CtlScale):
        self.footFKCtls = [] #FKコントローラーのリスト
        self.footFKCtlOffset = [] #FKコントローラーのオフセットリスト
        for footFKCtls in range(len(FKJoint)):
            self.footFKCtl = self.System.createRigController(self.System.TDcrc.TDCircle,FKJoint[footFKCtls],FKJoint[footFKCtls],CtlColor,15*CtlScale)
            if footFKCtls > 0:
                cmds.parent(self.footFKCtl[0],self.footFKCtls[footFKCtls-1])
            self.footFKCtls.append(self.footFKCtl[1])
            self.footFKCtlOffset.append(self.footFKCtl[0])
        self.footFKCtlGrp = self.System.createCenterPivotGP(self.footFKCtlOffset[0],"%s_Grp"%self.footFKCtls[0])
        #返り値は【Grp】,【Offset】,【Ctl】の順番
        return [self.footFKCtlGrp[0],self.footFKCtls[0],self.footFKCtls[1]]

    #IK制御用のコントローラーを作成
    def createFootIKCtl(self,IKjoint,CtlColor,CtlScale):
        self.footIKCtl = self.System.TDcrc.TDSquare("%s_Ctl"%IKjoint[-1])
        cmds.setAttr(self.footIKCtl+".overrideEnabled",1)
        cmds.setAttr(self.footIKCtl+".overrideColor",CtlColor)
        self.System.setNurbsCtlScaling(self.footIKCtl,10*CtlScale,15*CtlScale,15*CtlScale)
        self.footIKCtlOffset = self.System.createGP(self.footIKCtl,"%s_Offset"%self.footIKCtl)
        self.ctlPosition = cmds.xform(IKjoint[-1],q=True,ws=True,t=True)
        cmds.setAttr(self.footIKCtlOffset+".translate",self.ctlPosition[0],0,self.ctlPosition[2])
        self.getFootPivot = cmds.xform(IKjoint[-1],q=True,ws=True,rp=True)
        cmds.xform(self.footIKCtl,ws=True,piv=self.getFootPivot)
        self.footIKCtlGrp = self.System.createCenterPivotGP(self.footIKCtlOffset,"%s_Grp"%self.footIKCtl)

        return [self.footIKCtlGrp[0],self.footIKCtlOffset,self.footIKCtl]

    #IKハンドルの作成
    def createFootIKHandle(self,startJoint,endJoint,connectParent):
        self.footIKHandle = cmds.ikHandle(sj = startJoint,ee = endJoint,
                                sol="ikRPsolver",s="sticky",name="%s_ikHandle"%endJoint)
        self.footIKNull = self.System.createGP(self.footIKHandle[0],"ConnectionFrom__%s"%connectParent[-1])
        self.footIKGrp = self.System.createGP(self.footIKNull,"%s_IKHandle_Grp"%endJoint)
        cmds.xform(self.footIKGrp,piv=[0,0,0])

        return [self.footIKGrp,self.footIKNull,self.footIKHandle[0]]

    #IKの膝のコントローラー
    def createKneeIKCtl(self,IKjoint,CtlColor,CtlScale):
        self.kneeIKCtl = self.System.createRigController(self.System.TDcrc.TDsphere,IKjoint,IKjoint,CtlColor,1*CtlScale)
        self.getPivot = cmds.xform(IKjoint,q=True,ws=True,rp=True)
        cmds.xform(self.kneeIKCtl,ws=True,piv = self.getPivot)
        cmds.setAttr(self.kneeIKCtl[0]+".translateZ",self.getPivot[1])
        self.kneeIKCtlGrp = self.System.createCenterPivotGP(self.kneeIKCtl[0],"%s_Grp"%self.kneeIKCtl[1])

        return [self.kneeIKCtlGrp[0],self.kneeIKCtl[0],self.kneeIKCtl[1]]

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
        cmds.pointConstraint(self.kneeIKCtl[1],self.annotateNull)
        cmds.parentConstraint(footJoints,self.annotate)
        self.footAnnotateGrp = cmds.group(self.annotate,self.annotateNull,name="%sAnnotate_Grp"%footJoints)
        cmds.xform(self.footAnnotateGrp,piv=[0,0,0])

        return [self.footAnnotateGrp]

    #IKFKスイッチコントローラーを作成
    def createFootFKIKSwitchCtl(self,footJoints,CtlScale):
        self.FootFKIKSwitchCtl = self.System.createRigController(self.System.TDcrc.TDCross,"%sFKIKSwitch"%footJoints[-1],footJoints[0],20,1*CtlScale)
        self.getPosition = cmds.xform(footJoints[0],q=True,ws=True,rp=True)
        cmds.setAttr(self.FootFKIKSwitchCtl[0]+".rotateX",90)
        cmds.setAttr(self.FootFKIKSwitchCtl[0]+".translateX",self.getPosition[0]*3)
        cmds.pointConstraint(footJoints[0],self.FootFKIKSwitchCtl[1],mo=True)
        self.footFKIKSwitchCtlGrp = self.System.createCenterPivotGP(self.FootFKIKSwitchCtl[0],"%s_Grp"%self.FootFKIKSwitchCtl[1])

        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"t",1,0)
        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"r",1,0)
        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"s",1,0)
        self.System.createHideAttr(self.FootFKIKSwitchCtl[1],"v",1,0)

        return self.FootFKIKSwitchCtl[1]

    #IKFKスイッチコントローラーにFootアトリビュートを追加
    def addFootFKIKSwitchAttr(self,switchCtl):
        "Foot"
        cmds.addAttr(switchCtl,ln="Foot",at="enum",en="FK:FK_IK:IK:")
        cmds.setAttr(switchCtl+".Foot",k=True)
        self.FootSwitch = self.System.createStringAddAttr(switchCtl,"FK_IK","float","FK:IK:",1)
        self.FootSwitchCon1 = cmds.shadingNode("condition",asUtility=True,n="%sCondition1"%switchCtl)
        self.FootSwitchCon2 = cmds.shadingNode("condition",asUtility=True,n="%sCondition2"%switchCtl)
        cmds.connectAttr(self.FootSwitch,self.FootSwitchCon1+".firstTerm")
        cmds.connectAttr(self.FootSwitch,self.FootSwitchCon2+".firstTerm")
        cmds.connectAttr(self.FootSwitchCon1+".outColorR",self.FootSwitchCon2+".colorIfFalseR")
        cmds.connectAttr(self.FootSwitchCon2+".outColorR",switchCtl+".Foot")
        cmds.setAttr(self.FootSwitchCon2+".secondTerm",1)
        cmds.setAttr(self.FootSwitchCon2+".colorIfTrueR",2)

        return self.FootSwitch

    #Addジョイントへのコンストレイント関係
    def createFootAddJointConnection(self,footJoints,addJoint,FKjoint,IKjoint):
        self.FKBlendCList = []
        self.IKBlendCList = []
        for Joints in range(len(footJoints)):
            self.FKBlendC = cmds.orientConstraint(FKjoint[Joints],addJoint[Joints],mo=True,w=0)
            self.IKBlendC = cmds.orientConstraint(IKjoint[Joints],addJoint[Joints],mo=True,w=1)
            self.FKBlendCList.append(self.FKBlendC[0]+"."+FKjoint[Joints]+"W0")
            self.IKBlendCList.append(self.IKBlendC[0]+"."+IKjoint[Joints]+"W1")

    #FKコントローラーのコンストレイント関係
    def createFootFKConnection(self,footJoints,FKjoint):
        for Joints in range(len(footJoints)):
            self.System.matrixConstraint(self.footFKCtls[Joints],FKjoint[Joints])

    #IKコントローラーのコンストレイント関係
    def createFootIKConnection(self,footJoints,IKjoint,IKCtl,kneeIKCtl,footIKHandle):
        self.IKfootCtrpp = cmds.pointConstraint(IKCtl[-1],footIKHandle[1])
        self.IKfootCtrop = cmds.orientConstraint(IKCtl[-1],IKjoint[-1],mo=True)
        #極ベクトルの設定
        cmds.poleVectorConstraint(kneeIKCtl[-1],footIKHandle[-1])

    #FKIKスイッチコントローラーのコンストレイント関係
    def createFootFKIKSwitchConnection(self,footJoints,FKCtl,IKCtl,kneeIKCtl,IKHandle,annotate):#
        #コントローラーのVisibility
        self.reverse = cmds.shadingNode("reverse",asUtility=True,n="%sFKIKReverse"%footJoints[-1])
        self.IKcondition = cmds.shadingNode("condition",asUtility=True,n="%sIKcondition1"%footJoints[-1])
        self.FKcondition = cmds.shadingNode("condition",asUtility=True,n="%sFKcondition2"%footJoints[-1])
        cmds.connectAttr(self.FootSwitch,self.IKcondition+".firstTerm")
        cmds.connectAttr(self.FootSwitch,self.FKcondition+".firstTerm")
        cmds.setAttr(self.FKcondition+".secondTerm",1)
        cmds.connectAttr(self.FKcondition+".outColorR", FKCtl[0]+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", IKCtl[0]+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", kneeIKCtl[0]+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", IKHandle[0]+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", annotate[0]+".visibility")
        #コンストレイントのウエイト値
        cmds.connectAttr(self.FootSwitch, self.reverse+".inputX")
        for FKBlendCLists in self.FKBlendCList:
            cmds.connectAttr(self.reverse+".outputX",FKBlendCLists)
        for IKBlendCLists in self.IKBlendCList:
            cmds.connectAttr(self.FootSwitch,IKBlendCLists)

    """
    #足リグの階層分け
    def setFootRigLayering(self,footJoints):
        self.footIKCtlGP = cmds.group(self.IKFootCtrOffset,self.kneeIKCtl[0],name="%s_Ctl_Grp"%footJoints)
        cmds.xform(self.footIKCtlGP,piv=[0,0,0])
        self.footIKJointGP = cmds.group(self.footJoint[0],self.IKFootGP,self.FKFootGP,name="%s_Joint_Grp"%footJoints.split("_")[1])
        cmds.xform(self.footIKJointGP,piv=[0,0,0])
        cmds.setAttr(self.footIKJointGP+".visibility",0)
        self.annotateGrp = cmds.group(self.annotate,self.annotateNull,name="%sAnnotate_Grp"%footJoints)
        cmds.xform(self.annotateGrp,piv=[0,0,0])
        self.footCtlGP = cmds.group(self.footIKCtlGP,self.footFKCtlGP,name="%s_Ctl_Grp"%self.footJoint[-1].split("Add_")[1])
        cmds.xform(self.footCtlGP,piv=[0,0,0])
        self.footFKIKSwitchCtlGP = cmds.group(self.FootFKIKSwitchCtl[0],name="%sFKIKSwitch_Ctl_Grp"%self.footJoint[-1].split("Add_")[1])
        cmds.xform(self.footFKIKSwitchCtlGP,piv=[0,0,0])

        return [self.footCtlGP, self.footIKJointGP,self.annotateGrp,self.footFKIKSwitchCtlGP]
    """
