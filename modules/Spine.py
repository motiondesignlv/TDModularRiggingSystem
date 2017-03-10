#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#背骨のリギング
class TDSpineRigging():
    def __init__(self):
        #TDMRS.__init__()
        self.System  = System.ModularRiggingSystem()
        self.spineCtls    = [] #背骨コントローラー
        self.spineIKCtls  = []
        self.spineCtlOffset  = [] #背骨コントローラーのオフセットノード
        self.spineIKCtlOffset = []
        self.spineCtlNull = [] #背骨コントローラーのヌルノード
        self.spineNull    = [] #背骨ジョイントのオフセットノード
        self.spineIKLoc   = [] #スプラインIK制御用のロケーター

    #背骨リグ用の新しいジョイントを作成
    def createSpineJoint(self,spineJoints):
        self.spineJoint = self.System.createRiggingJoint(spineJoints,1,"Add")

        return self.spineJoint

    #FKの背骨のジョイントを作成
    def createSpineFKJoint(self,spineJoints):
        self.FKSpineJoint = self.System.createRiggingJoint(spineJoints,0,"FK")

        return self.FKSpineJoint

    #IKの背骨のジョイントを作成
    def createSpineIKJoint(self,spineJoints):
        self.IKSpineJoint = self.System.createRiggingJoint(spineJoints,0,"IK")

        return self.IKSpineJoint

    #背骨のIKスプラインを作成
    def createSpineIKHandle(self,spineJoints):
        self.pos = []
        for spineIK in spineJoints:
            self.pointPP = cmds.xform(spineIK,q=True,ws=True,t=True)
            self.pos.append(self.pointPP)

        self.curve = cmds.curve(n="%s_Curve"%spineJoints[1],d=1,p=self.pos)

        self.spineIKSplineSolver = cmds.ikHandle( sol="ikSplineSolver",n="spine_ikSplineSolver",sj=spineJoints[0],ee=spineJoints[-1],c=self.curve,fj=True )
        cmds.rebuildCurve(self.curve,s=2)

        self.curveShape = cmds.listRelatives(self.curve,s=True)
        self.cv = cmds.getAttr(self.curveShape[0]+".spans") + cmds.getAttr(self.curveShape[0]+".degree")

        self.splineIkLoc = []
        for cvs in range(self.cv):
            self.cvPos = cmds.pointPosition(self.curveShape[0]+".cv[%d]"%cvs)
            self.loc = cmds.spaceLocator(p=self.cvPos,n="ikSplineLocator_0%d"%(cvs+1))[0]
            self.locShape = cmds.listRelatives(self.loc,s=True)
            cmds.connectAttr(self.locShape[0]+".worldPosition[0]",self.curveShape[0]+".controlPoints[%d]"%cvs)
            self.piv = cmds.xform(self.loc,piv=self.cvPos)
            self.splineIkLoc.append(self.loc)

        cmds.parent(self.splineIkLoc[1],self.splineIkLoc[0])
        cmds.parent(self.splineIkLoc[3],self.splineIkLoc[4])
        self.spineIKLoc.append(self.splineIkLoc[0])
        self.spineIKLoc.append(self.splineIkLoc[2])
        self.spineIKLoc.append(self.splineIkLoc[-1])
        self.IKSplineGP = self.System.createCenterPivotGP([self.spineIKSplineSolver[0],self.curve],"%s_Grp"%self.spineIKSplineSolver[0])

        return self.IKSplineGP

    #FKの背骨のコントローラーの作成
    def createSpineFKCtl(self,spineJoints,CtlColor,CtlScale):
        for spines in range(len(spineJoints)):
            self.spineCtl = self.System.createRigController(self.System.TDcrc.TDCircle,"FK_"+spineJoints[spines],spineJoints[spines],CtlColor,20*CtlScale)
            if spines > 0:
                cmds.parent(self.spineCtl[0],self.spineCtls[spines-1])
            self.spineCtls.append(self.spineCtl[1])
            self.spineCtlOffset.append(self.spineCtl[0])

        self.spineCtlGP = self.System.createCenterPivotGP(self.spineCtlOffset[0],"%s_Grp"%self.spineCtls[0])
        return [self.spineCtlGP, self.spineCtls[-1]]

    #IKの背骨のコントローラーの作成
    def createSpineIKCtl(self,spineJoints,CtlColor,CtlScale):
        for spines in range(len(self.spineIKLoc)):
            self.spineIKCtl = self.System.createRigController(self.System.TDcrc.TDCube,"IK_"+spineJoints[spines],self.spineIKLoc[spines],CtlColor,20*CtlScale)
            cmds.setAttr(self.spineIKCtl[0]+".scale",2,0.3,2)
            cmds.makeIdentity(self.spineIKCtl[0],apply=True,s=True)
            #if spines > 0:
                #cmds.parent(self.spineIKCtl[0],self.spineIKCtls[spines-1])
            self.spineIKCtls.append(self.spineIKCtl[1])
            self.spineIKCtlOffset.append(self.spineIKCtl[0])
            cmds.parent(self.spineIKLoc[spines],self.spineIKCtl[1])

        self.spineIKCtlGP = self.System.createCenterPivotGP(self.spineIKCtlOffset,"%s_Grp"%self.spineIKCtls[0])
        return [self.spineIKCtlGP, self.spineIKCtls[-1]]

    #FK背骨コントローラーの関連付け
    def createSpineFKCtlConnection(self,spineJoints):
        self.FKBlendCList = []
        for spines in range(len(spineJoints)):
            self.FKBlendC = cmds.parentConstraint(self.FKSpineJoint[spines],self.spineJoint[spines],mo=True)
            self.FKBlendJ = cmds.parentConstraint(self.spineCtls[spines],self.FKSpineJoint[spines],mo=True)
            #self.System.matrixConstraint(self.FKSpineJoint[spines],self.spineJoint[spines])
            #self.System.matrixConstraint(self.spineCtls[spines],self.FKSpineJoint[spines])
            self.FKBlendCList.append(self.FKBlendC[0]+"."+self.FKSpineJoint[spines]+"W0")

        return self.FKBlendCList

    #IK背骨コントローラーの関連付け
    def createSpineIKCtlConnection(self,spineJoints):
        self.IKBlendCList = []
        for spines in range(len(spineJoints)):
            self.IKBlendC = cmds.parentConstraint(self.IKSpineJoint[spines+1],self.spineJoint[spines],mo=True)
            #cmds.parentConstraint(self.spineCtls[spines],self.IKSpineJoint[spines],mo=True)
            self.IKBlendCList.append(self.IKBlendC[0]+"."+self.IKSpineJoint[spines+1]+"W1")
        cmds.orientConstraint(self.spineIKLoc[-1],self.IKSpineJoint[-1],mo=True)

        return self.IKBlendCList

    #IKFKスイッチコントローラーを作成
    def createSpineFKIKSwitchCtl(self,spineJoints,CtlScale):
        self.SpineFKIKSwitchCtl = self.System.createRigController(self.System.TDcrc.TDCross,"%sFKIKSwitch"%spineJoints[0],spineJoints[1],20,1*CtlScale)
        self.getPosition1 = cmds.xform(self.IKSpineJoint[0],q=True,ws=True,rp=True)
        self.getPosition2 = cmds.xform(self.IKSpineJoint[-1],q=True,ws=True,rp=True)
        self.getPosition = [self.getPosition1[0]-self.getPosition2[0],self.getPosition1[1]-self.getPosition2[1],self.getPosition1[2]-self.getPosition2[2]]
        cmds.setAttr(self.SpineFKIKSwitchCtl[0]+".rotateX",90)
        cmds.setAttr(self.SpineFKIKSwitchCtl[0]+".translateX",-self.getPosition[1]*1)
        cmds.pointConstraint(self.spineJoint[1],self.SpineFKIKSwitchCtl[1],mo=True)

        self.System.createHideAttr(self.SpineFKIKSwitchCtl[1],"t",1,0)
        self.System.createHideAttr(self.SpineFKIKSwitchCtl[1],"r",1,0)
        self.System.createHideAttr(self.SpineFKIKSwitchCtl[1],"s",1,0)
        self.System.createHideAttr(self.SpineFKIKSwitchCtl[1],"v",1,0)

        self.gp = self.System.createCenterPivotGP(self.SpineFKIKSwitchCtl[0],"%s_Grp"%self.SpineFKIKSwitchCtl[1])

        return self.gp

    #IKFKスイッチコントローラーにSpineアトリビュートを追加
    def addSpineFKIKSwitchAttr(self):
        self.name = "Spine"
        cmds.addAttr(self.SpineFKIKSwitchCtl[1],ln=self.name,at="enum",en="FK:FK_IK:IK:")
        cmds.setAttr(self.SpineFKIKSwitchCtl[1]+".%s"%self.name,k=True)
        self.SpineSwitch = self.System.createStringAddAttr(self.SpineFKIKSwitchCtl[1],"FK_IK","float","FK:IK:",1)
        self.SpineSwitchCon1 = cmds.shadingNode("condition",asUtility=True,n="%sCondition1"%self.SpineFKIKSwitchCtl[1])
        self.SpineSwitchCon2 = cmds.shadingNode("condition",asUtility=True,n="%sCondition2"%self.SpineFKIKSwitchCtl[1])
        cmds.connectAttr(self.SpineSwitch,self.SpineSwitchCon1+".firstTerm")
        cmds.connectAttr(self.SpineSwitch,self.SpineSwitchCon2+".firstTerm")
        cmds.connectAttr(self.SpineSwitchCon1+".outColorR",self.SpineSwitchCon2+".colorIfFalseR")
        cmds.connectAttr(self.SpineSwitchCon2+".outColorR",self.SpineFKIKSwitchCtl[1]+".%s"%self.name)
        cmds.setAttr(self.SpineSwitchCon2+".secondTerm",1)
        cmds.setAttr(self.SpineSwitchCon2+".colorIfTrueR",2)

        return self.SpineSwitch

    #FKIKスイッチコントローラーのコンストレイント関係
    def createSpineFKIKSwitchConnection(self,spineJoints):
        #コントローラーのVisibility
        self.reverse = cmds.shadingNode("reverse",asUtility=True,n="%sFKIKReverse"%spineJoints[-1])
        self.IKcondition = cmds.shadingNode("condition",asUtility=True,n="%sIKcondition1"%spineJoints[-1])
        self.FKcondition = cmds.shadingNode("condition",asUtility=True,n="%sFKcondition2"%spineJoints[-1])
        cmds.connectAttr(self.SpineSwitch,self.IKcondition+".firstTerm")
        cmds.connectAttr(self.SpineSwitch,self.FKcondition+".firstTerm")
        cmds.setAttr(self.FKcondition+".secondTerm",1)
        cmds.connectAttr(self.FKcondition+".outColorR", self.spineCtlGP[0]+".visibility")
        cmds.connectAttr(self.IKcondition+".outColorR", self.spineIKCtlGP[0]+".visibility")
        #cmds.connectAttr(self.IKcondition+".outColorR", self.footIKGP+".visibility")
        #cmds.connectAttr(self.IKcondition+".outColorR", self.annotateGrp+".visibility")

        #コンストレイントのウエイト値
        cmds.connectAttr(self.SpineSwitch, self.reverse+".inputX")
        for FKBlendCLists in self.FKBlendCList:
            cmds.connectAttr(self.reverse+".outputX",FKBlendCLists)
        for IKBlendCLists in self.IKBlendCList:
            cmds.connectAttr(self.SpineSwitch,IKBlendCLists)

    #親となるモジュールとの関連付け用のヌルを作成
    def createSpineRigConnectParentNull(self,parentJoints):
        self.ConnectionGrp = self.System.createModuleConnectionNull([self.spineCtlGP[0],self.spineIKCtlGP[0]], parentJoints)

        return self.ConnectionGrp

    #背骨リグの階層分け
    def createSpineRigConnectNull(self,spineJoints):
        #self.ConnectionGrp = self.System.createModuleConnectionNull(self.spineCtlGP, spineJoints)
        self.spineCtlGrp = self.System.createCenterPivotGP(self.ConnectionGrp,name="%s_Ctl_Grp"%spineJoints[0])
        self.spineJointGrp = self.System.createCenterPivotGP([self.spineJoint[0],self.FKSpineJoint[0],self.IKSpineJoint[0]],name="%s_Joint_Grp"%spineJoints[0])

        return self.spineCtlGrp,self.spineJointGrp
