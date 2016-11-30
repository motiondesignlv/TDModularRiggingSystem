#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#頭のリギング
class TDNeckRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()
        self.neckCtls    = [] #首コントローラー
        self.neckCtlOffset    = [] #首オフセットコントローラー

    "-----コマンドの実行-----"
    def setNeckRigging(self,neckJoints,CtlColor):#,CtlName,parentName
        TDNeckRigging.createNeckJoint(self,neckJoints)
        self.NeckCtlList = TDNeckRigging.createNeckFKCtl(self,neckJoints,CtlColor)
        """
        TDNeckRigging.createHeadCtlConnection(self)
        self.spineConstraintGPList = TDNeckRigging.createSpineCtlConstraint(self,parentName)

        print "--result Neck setup--\n",
        return self.NeckCtlList + [self.spineConstraintGPList]
        """

    #首リグ用の新しいジョイントを作成
    def createNeckJoint(self,neckJoints):
        self.neckJoint = self.TDMRS.createRiggingJoint(neckJoints,1,"Add")

        return self.neckJoint

    #FKの背骨のコントローラーの作成
    def createNeckFKCtl(self,neckJoints,CtlColor):
        for necks in range(len(neckJoints)):
            self.neckCtl = self.TDMRS.createMatrixRigController(self.TDMRS.TDcrc.TDCircle,neckJoints[necks],neckJoints[necks],CtlColor,15)
            if necks > 0:
                cmds.parent(self.neckCtl[0],self.neckCtls[necks-1])
            self.neckCtls.append(self.neckCtl[1])
            self.neckCtlOffset.append(self.neckCtl[0])

        self.neckCtlGP = self.TDMRS.createGP(self.neckCtlOffset[0],"%s_Grp"%self.neckCtls[0])
        return [self.neckCtlGP, self.neckCtls[-1]]


    #FKの首のコントローラー
    def createFKNeckCtl(self,neckJoints,CtlColor):
        self.neckCtl = self.TDMRS.createMatrixRigController(self.TDMRS.TDcrc.TDCircle,neckJoints,neckJoints,CtlColor,15)
        #self.neckJointGP = self.TDMRS.createChildAttrToParentGP(neckJoints,"%sConnection_From__%s"%(neckJoints,self.neckCtl))
        #self.neckCtlGP = self.TDMRS.createGP(self.neckCtl,"%s_GP"%self.neckCtl)
        #self.neckCtlOffset = self.TDMRS.createChildAttrToParentGP(self.neckCtl,"%s_Offset"%self.neckCtl)

        #return [self.neckCtlGP, self.neckCtl]

    #FKの頭のコントローラーの関連づけ
    def createHeadCtlConnection(self,*argv):
        self.neckCtlMtx = self.TDMRS.matrixConstraint(self.neckCtl,self.neckJointGP)

        return self.neckCtlMtx

    #背骨ジョイント関連づけ用のヌルを作成
    def createSpineCtlConstraint(self,parentName):
        self.spineConstraintGP = self.TDMRS.createModuleParentNull(parentName,self.neckCtlOffset)

        return self.spineConstraintGP
