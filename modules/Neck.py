#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#頭のリギング
class TDNeckRigging():
    def __init__(self):
        self.System  = System.ModularRiggingSystem()
        self.neckCtls    = [] #首コントローラー
        self.neckCtlOffset    = [] #首オフセットコントローラー

    #首リグ用の新しいジョイントを作成
    def createNeckJoint(self,neckJoints):
        self.neckJoint = self.System.createRiggingJoint(neckJoints,1,"Add")

        return self.neckJoint

    #FKの首のコントローラーの作成
    def createNeckFKCtl(self,neckJoints,CtlColor,CtlScale):
        for necks in range(len(neckJoints)):
            self.neckCtl = self.System.createMatrixRigController(self.System.TDcrc.TDCircle,"FK_"+neckJoints[necks],neckJoints[necks],CtlColor,15*CtlScale)
            if necks > 0:
                cmds.parent(self.neckCtl[0],self.neckCtls[necks-1])
            self.neckCtls.append(self.neckCtl[1])
            self.neckCtlOffset.append(self.neckCtl[0])

        self.neckCtlGP = self.System.createGP(self.neckCtlOffset[0],"%s_Grp"%self.neckCtls[0].split("FK_")[1])
        return [self.neckCtlGP, self.neckCtls[-1]]

    #FKの首のコントローラーの関連づけ
    def setNeckCtlConnection(self,neckJoints):
        for neckJts in range(len(neckJoints)):
            self.neckCtlMtx = self.System.matrixConstraint(self.neckCtls[neckJts],self.neckJoint[neckJts])

        return self.neckCtlMtx

    #首リグの階層分け
    def createNeckRigConnectNull(self,spineJoints):
        self.ConnectionGrp = self.System.createModuleConnectionNull(self.neckCtlOffset[0],spineJoints)
        #self.neckCtlGrp = cmds.group(self.ConnectionGrp,name="%s_Ctl_Grp"%spineJoints)
        #self.spineJointGrp = cmds.group(self.spineJoint[0],self.FKSpineJoint[0],name="%s_Joint_Grp"%spineJoints)

        return self.ConnectionGrp

"""
    #背骨ジョイント関連づけ用のヌルを作成
    def createSpineCtlConstraint(self,parentName):
        self.spineConstraintGP = self.System.createModuleParentNull(parentName,self.neckCtlOffset)

        return self.spineConstraintGP
"""
