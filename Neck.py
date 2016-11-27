#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#頭のリギング
class TDHeadRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    def setHeadRigging(self,CtlName,parentName,CtlColor):
        self.NeckCtlList = TDHeadRigging.createFKNeckCtl(self,CtlName,CtlColor)
        TDHeadRigging.createHeadCtlConnection(self)
        self.spineConstraintGPList = TDHeadRigging.createSpineCtlConstraint(self,parentName)

        print "--result Neck setup--\n",
        return self.NeckCtlList + [self.spineConstraintGPList]

    #FKの首のコントローラー
    def createFKNeckCtl(self,CtlName,CtlColor):
        self.neckCtl = self.TDMRS.createMatrixRigController(self.TDMRS.TDcrc.TDCircle,CtlName,CtlName,CtlColor,15)
        self.neckJointGP = self.TDMRS.createChildAttrToParentGP(CtlName,"%sConnection_From__%s"%(CtlName,self.neckCtl))
        self.neckCtlGP = self.TDMRS.createGP(self.neckCtl,"%s_GP"%self.neckCtl)
        self.neckCtlOffset = self.TDMRS.createChildAttrToParentGP(self.neckCtl,"%s_Offset"%self.neckCtl)

        return [self.neckCtlGP, self.neckCtl]

    #FKの頭のコントローラーの関連づけ
    def createHeadCtlConnection(self,*argv):
        self.neckCtlMtx = self.TDMRS.matrixConstraint(self.neckCtl,self.neckJointGP)

        return self.neckCtlMtx

    #背骨ジョイント関連づけ用のヌルを作成
    def createSpineCtlConstraint(self,parentName):
        self.spineConstraintGP = self.TDMRS.createModuleParentNull(parentName,self.neckCtlOffset)

        return self.spineConstraintGP
