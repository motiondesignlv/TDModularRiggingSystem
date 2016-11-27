#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#頭のリギング
class TDHeadRigging():
    def __init__(self):
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    #CtlName: コントローラー名, parentName: 親の名前, CtlColor:　コントローラーのカラー
    def setHeadRigging(self,CtlName,parentName,CtlColor):
        self.HeadCtlList = TDHeadRigging.createFKHeadCtl(self,CtlName,CtlColor)
        TDHeadRigging.createHeadCtlConnection(self)
        self.neckConstraintGPList = TDHeadRigging.createNeckCtlConstraint(self,parentName)

        return [self.HeadCtlList, self.neckConstraintGPList]

    #FKの頭のコントローラー
    def createFKHeadCtl(self,CtlName,CtlColor):
        self.headCtl = self.TDMRS.createMatrixRigController(self.TDMRS.TDcrc.TDCircle,CtlName,CtlName,CtlColor,15)
        self.headJointGP = self.TDMRS.createChildAttrToParentGP(CtlName,"%sConnection_From__%s"%(CtlName,self.headCtl))
        self.headCtlGP = self.TDMRS.createGP(self.headCtl,"%s_GP"%self.headCtl)
        self.headCtlOffset = self.TDMRS.createChildAttrToParentGP(self.headCtl,"%s_Offset"%self.headCtl)

        return self.headCtlGP

    #FKの頭のコントローラーの関連づけ
    def createHeadCtlConnection(self,*argv):
        self.headCtlMtx = self.TDMRS.matrixConstraint(self.headCtl,self.headJointGP)

        return self.headCtlMtx

    #首ジョイント関連づけ用のヌルを作成
    def createNeckCtlConstraint(self,parentName):
        self.neckConstraintGP = self.TDMRS.createModuleParentNull(parentName,self.headCtlOffset)

        return self.neckConstraintGP
