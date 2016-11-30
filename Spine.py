#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#背骨のリギング
class TDSpineRigging():
    def __init__(self):
        #TDMRS.__init__()
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()
        self.spineCtls    = [] #背骨コントローラー
        self.spineCtlNull = [] #背骨コントローラーのオフセットノード
        self.spineNull    = [] #背骨ジョイントのオフセットノード

    "-----コマンドの実行-----"
    def setSpineRigging(self,parentName,CtlColor):
        self.SpineCtlList = TDSpineRigging.createFKSpineCtl(self,CtlColor)
        TDSpineRigging.createFKSpineCtlConnection(self)
        #TDSpineRigging.createSpineNull(self)
        TDSpineRigging.setSpineCtlLayering(self)
        #TDSpineRigging.createSpineCtlNull(self)
        self.rootConstraintGPList = TDSpineRigging.createRootCtlConstraint(self,parentName)

        print "--result spine setup--\n",
        return self.SpineCtlList + [self.rootConstraintGPList]

    #FKの背骨のコントローラーの作成
    def createFKSpineCtl(self,CtlColor):
        for spines in self.TDMRS.getSpineJoint():
            self.spineCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCircle,spines,spines,CtlColor,20)
            self.spineCtls.append(self.spineCtl)

        self.spineCtlGP = self.TDMRS.createGP(self.spineCtls[0],"%s_GP"%self.spineCtls[0])
        return [self.spineCtlGP, self.spineCtls[-1]]

    #FK背骨コントローラーの関連付け
    def createFKSpineCtlConnection(self):
        for spines in range(len(self.TDMRS.getSpineJoint())):
            cmds.parentConstraint(self.spineCtls[spines],self.TDMRS.getSpineJoint()[spines],mo=True)

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

    #背骨のコントローラーの階層分け
    def setSpineCtlLayering(self):
        self.spineCtls.reverse()
        for spineLayers in range(len(self.spineCtls)-1):
            cmds.parent(self.spineCtls[spineLayers],self.spineCtls[spineLayers+1])
        self.spineCtls.reverse()

    #ルートコントローラー関連づけ用のヌルを作成
    def createRootCtlConstraint(self,parentName):
        self.rootConstraintGP = self.TDMRS.createModuleParentNull(parentName,self.spineCtls[0])

        return self.rootConstraintGP
