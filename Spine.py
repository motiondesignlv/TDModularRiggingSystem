#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#背骨のリギング
class TDSpineRigging():
    def __init__(self):
        #TDMRS.__init__()
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()
        self.spineCtls    = [] #背骨コントローラー
        self.spineCtlOffset  = [] #背骨コントローラーのオフセットノード
        self.spineCtlNull = [] #背骨コントローラーのヌルノード
        self.spineNull    = [] #背骨ジョイントのオフセットノード

    "-----コマンドの実行-----"
    def setSpineRigging(self,spineJoints,CtlColor):#,parentName,
        TDSpineRigging.createSpineJoint(self,spineJoints)
        TDSpineRigging.createSpineFKJoint(self,spineJoints)
        self.SpineCtlList = TDSpineRigging.createSpineFKCtl(self,spineJoints,CtlColor)
        TDSpineRigging.createSpineFKCtlConnection(self,spineJoints)
        self.SpineJointGrp = TDSpineRigging.setSpineRigLayering(self,spineJoints[0])
        #TDSpineRigging.createSpineNull(self)
        #TDSpineRigging.createSpineCtlNull(self)
        #self.rootConstraintGPList = TDSpineRigging.createRootCtlConstraint(self,parentName)

        print "--result spine setup--\n",
        return [self.SpineCtlList[0],self.SpineCtlList[1],self.SpineJointGrp]

    #背骨リグ用の新しいジョイントを作成
    def createSpineJoint(self,spineJoints):
        self.spineJoint = self.TDMRS.createRiggingJoint(spineJoints,1,"Add")

        return self.spineJoint

    #FKの背骨のジョイントを作成
    def createSpineFKJoint(self,spineJoints):
        self.FKSpineJoint = self.TDMRS.createRiggingJoint(spineJoints,0,"FK")

        return self.FKSpineJoint

    #FKの背骨のコントローラーの作成
    def createSpineFKCtl(self,spineJoints,CtlColor):
        for spines in range(len(spineJoints)):
            self.spineCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCircle,spineJoints[spines],spineJoints[spines],CtlColor,20)
            if spines > 0:
                cmds.parent(self.spineCtl[0],self.spineCtls[spines-1])
            self.spineCtls.append(self.spineCtl[1])
            self.spineCtlOffset.append(self.spineCtl[0])

        self.spineCtlGP = self.TDMRS.createGP(self.spineCtlOffset[0],"%s_Grp"%self.spineCtls[0])
        return [self.spineCtlGP, self.spineCtls[-1]]

    #FK背骨コントローラーの関連付け
    def createSpineFKCtlConnection(self,spineJoints):
        for spines in range(len(spineJoints)):
            #cmds.parentConstraint(self.FKSpineJoint[spines],self.spineJoint[spines],mo=True)
            #cmds.parentConstraint(self.spineCtls[spines],self.FKSpineJoint[spines],mo=True)
            self.TDMRS.matrixConstraint(self.FKSpineJoint[spines],self.spineJoint[spines])
            self.TDMRS.matrixConstraint(self.spineCtls[spines],self.FKSpineJoint[spines])

    #背骨リグの階層分け
    def setSpineRigLayering(self,spineJoints):
        self.spineJointGrp = cmds.group(self.spineJoint[0],self.FKSpineJoint[0],name="%s_Joint_Grp"%spineJoints)

        return self.spineJointGrp
    """
    #背骨ジョイントのオフセットノードを作成
    def createSpineNull(self):
        for spineNulls in self.getSpineJoint():
            self.spineNullGP = self.createGP(spineNulls,"%s_Offset"%spineNulls)
            self.spineNull.append(self.spineNullGP)

    #背骨コントローラーのオフセットノードを作成
    def createSpineCtlNull(self):
        for spineCtlNulls in self.spineCtls:
            self.spineCtlNullGP = self.createGP(spineCtlNulls,"%s_Offset"%spineNulls)
            self.spineCtlNull.append(self.spineCtlNullGP)

    #ルートコントローラー関連づけ用のヌルを作成
    def createRootCtlConstraint(self,parentName):
        self.rootConstraintGP = self.TDMRS.createModuleParentNull(parentName,self.spineCtls[0])

        return self.rootConstraintGP
    """
