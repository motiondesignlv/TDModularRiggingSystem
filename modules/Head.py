#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem.lib import System as System

#頭のリギング
class TDHeadRigging():
    def __init__(self):
        self.System  = RiggingSystem.ModularRiggingSystem()

    "-----コマンドの実行-----"
    #CtlName: コントローラー名, parentName: 親の名前, CtlColor:　コントローラーのカラー
    def setHeadRigging(self,CtlName,parentName,CtlColor):
        self.HeadCtlList = TDHeadRigging.createFKHeadCtl(self,CtlName,CtlColor)
        TDHeadRigging.createHeadCtlConnection(self)
        self.neckConstraintGPList = TDHeadRigging.createNeckCtlConstraint(self,parentName)

        return [self.HeadCtlList, self.neckConstraintGPList]

    #FKの頭のコントローラー
    def createFKHeadCtl(self,CtlName,CtlColor):
        self.headCtl = self.System.createMatrixRigController(self.System.TDcrc.TDCircle,CtlName,CtlName,CtlColor,15)
        self.headJointGP = self.System.createChildAttrToParentGP(CtlName,"%sConnection_From__%s"%(CtlName,self.headCtl))
        self.headCtlGP = self.System.createGP(self.headCtl,"%s_GP"%self.headCtl)
        self.headCtlOffset = self.System.createChildAttrToParentGP(self.headCtl,"%s_Offset"%self.headCtl)

        return self.headCtlGP

    #FKの頭のコントローラーの関連づけ
    def createHeadCtlConnection(self,*argv):
        self.headCtlMtx = self.System.matrixConstraint(self.headCtl,self.headJointGP)

        return self.headCtlMtx

    #首ジョイント関連づけ用のヌルを作成
    def createNeckCtlConstraint(self,parentName):
        self.neckConstraintGP = self.System.createModuleParentNull(parentName,self.headCtlOffset)

        return self.neckConstraintGP
