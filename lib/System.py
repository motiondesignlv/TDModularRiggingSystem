# -*- coding: utf-8 -*-

import maya.cmds as cmds
from TDModularRiggingSystem.lib import Controller as Controller

reload(Controller)

class ModularRiggingSystem(object):
    def __init__(self):
        self.TDcrc       = Controller.TDCreateRigController()
        self.selHJ       = cmds.ls(sl=True,dag=True,type="joint") #選択したジョイント階層をすべて取得
        self.jointLabel  = {} #ジョイントのラベル情報の辞書
        self.jointRotate = {} #回転値が入ったジョイントを辞書で返す
        if self.selHJ == []:
            cmds.error(u"ジョイントを選択して下さい")

    "-----値の取得-----"
    #ジョイントのラベル情報を取得
    def getJointLabelType(self):
        for self.selHJs in self.selHJ:
            """ 中央=0, 左側=1, 右側=2, なし=3 """
            self.jointSide = cmds.getAttr(self.selHJs+".side")#ジョイントのサイド
            self.jointType = cmds.getAttr(self.selHJs+".type")#ジョイントのタイプ
            self.jointLabel[self.jointSide,self.jointType] = self.selHJs
        return self.jointLabel

    #首のジョイントを取得
    def getNeckJoint(self):
        self.neckJoint = [] #背骨ジョイント
        for self.selHJs in self.selHJ:
            self.jointSide = cmds.getAttr(self.selHJs+".side")#ジョイントのサイド
            self.jointType = cmds.getAttr(self.selHJs+".type")#ジョイントのタイプ
            if self.jointType == 7:
                self.neckJoint.append(self.selHJs)
        return self.neckJoint

    #背骨のジョイントを取得
    def getSpineJoint(self):
        self.spineJoint = [] #背骨ジョイント
        for self.selHJs in self.selHJ:
            self.jointSide = cmds.getAttr(self.selHJs+".side")#ジョイントのサイド
            self.jointType = cmds.getAttr(self.selHJs+".type")#ジョイントのタイプ
            if self.jointType == 6:
                self.spineJoint.append(self.selHJs)
        return self.spineJoint

    #指定したジョイント間のジョイント名を取得
    def getBetweenJoint(self,first,last):
        self.btJoint = set(cmds.ls(first,dag=True)) - set(cmds.ls(last,dag=True))
        self.stJoint = sorted(self.btJoint,key=cmds.ls(first,dag=True).index)
        self.stJoint.extend([last])
        return self.stJoint

    #回転値の入ったジョイントを取得
    def getJointRotate(self):
        for self.selHJs in self.selHJ:
            self.jointR = cmds.getAttr(self.selHJs+".rotate")
            self.jointRotate[self.selHJs] = self.jointR[0]
        return self.jointRotate

    #ジョイントのワールド位置を取得
    def getJointWPosition(self,node):
        return cmds.joint(node,q=True,r=True,p=True)

    "-----コマンドの補助-----"
    #子供のピボットポイントのヌルを作成
    def createGP(self,node,name):
        self.getPivot = cmds.xform(node,q=True,ws=True,rp=True)
        self.gp = cmds.group(node,n="%s"%name,r=True)
        cmds.xform(self.gp,ws=True,piv = self.getPivot)
        return self.gp

    #子供のアトリビュートを作成した親ヌルへ
    def createChildAttrToParentGP(self,node,name):
        self.parentGP = self.createGP(node,name)
        self.getPivot = cmds.xform(self.parentGP,q=True,ws=True,rp=True)
        self.getT = cmds.getAttr(node+".translate")[0]
        self.getR = cmds.getAttr(node+".rotate")[0]
        self.getS = cmds.getAttr(node+".scale")[0]
        cmds.setAttr(node+".translate",0,0,0)
        cmds.setAttr(node+".rotate",0,0,0)
        cmds.setAttr(node+".scale",1,1,1)
        cmds.setAttr(self.parentGP+".translate",*self.getT)
        cmds.setAttr(self.parentGP+".rotate",*self.getR)
        cmds.setAttr(self.parentGP+".scale",*self.getS)
        cmds.xform(self.parentGP,ws=True,piv = self.getPivot)
        return self.parentGP

    #リグのヌル階層を作成
    def createRigHierarchy(self):
        self.RootGP = cmds.group(n="Root",em=True)
        self.GP1Name = ["Geometry_GP","Motion_GP"]
        self.GP2Name = ["Joint_GP","Ctl_GP","MotionSystem_GP"]
        self.GP3Name = ["JointSystem_GP","IKSystem_GP","FKIKSystem_GP"]
        for GP1 in range(len(self.GP1Name)):
            cmds.group(n="%s"%self.GP1Name[GP1],em=True,p=self.RootGP)
        for GP2 in range(len(self.GP2Name)):
            cmds.group(n="%s"%self.GP2Name[GP2],em=True,p=self.GP1Name[-1])
        for GP3 in range(len(self.GP3Name)):
            cmds.group(n="%s"%self.GP3Name[GP3],em=True,p=self.GP2Name[-1])
        return cmds.ls(self.RootGP,dag=True)

    #リグのコントローラーを作成し、色、大きさを変更
    #name : メソッド名 , CtlName　：　コントローラー名 , pcName : コンストレイントの親 , color : 色　, scale : スケール
    def createRigController(self,name,CtlName,pcName,color,scale):
        self.RigCtr = name("%s_Ctl"%CtlName)
        cmds.setAttr(self.RigCtr+".overrideEnabled",1)
        cmds.setAttr(self.RigCtr+".overrideColor",color)
        cmds.setAttr(self.RigCtr+".scale",scale,scale,scale)
        cmds.makeIdentity(self.RigCtr,apply=True,t=1,r=1,s=1)
        self.ctlOffsetGP = cmds.group(self.RigCtr,n="%s_Offset"%self.RigCtr)
        cmds.xform(self.ctlOffsetGP,piv=[0,0,0])
        self.pc = cmds.xform(pcName,q=True,ws=True,rp=True)
        cmds.setAttr(self.ctlOffsetGP+".translate",*self.pc)
        #cmds.makeIdentity(self.RigCtr,apply=True,t=1,r=1,s=1)
        return [self.ctlOffsetGP,self.RigCtr]

    #アトリビュートの非表示とロック
    #name : メソッド名 , attrName　：　アトリビュート名 , lock : ロック , hide : 非表示
    def createHideAttr(self,name,attrName,lock,hide):
        self.listHideAttr = ["x","y","z"]
        if attrName == "t" or attrName == "r" or attrName == "s":
            for listHideAttrs in self.listHideAttr:
                cmds.setAttr("%s.%s%s"%(name,attrName,listHideAttrs),l=lock,k=hide,cb=hide)
        else:
             cmds.setAttr("%s.v"%(name),l=lock,k=hide,cb=hide)

    #アトリビュートの作成
    def createAddAttr(self,name,longName,attrName,min=0,max=0,dv=0):
        cmds.addAttr(name,ln=longName,at=attrName,min=min,max=max,dv=dv)
        cmds.setAttr(name+"."+longName,k=True)
        return name+"."+longName

    #文字列アトリビュートの作成
    def createStringAddAttr(self,name,longName,attrName,enum,dv=0,min=0,max=1):
        cmds.addAttr(name,ln=longName,at=attrName,en=enum,dv=dv,min=min,max=max)
        cmds.setAttr(name+"."+longName,k=True)
        return name+"."+longName

    #マトリックスコンストレイント
    def matrixConstraint(self,parents,childs,t=True,r=True,s=True):
        self.multMatrix = cmds.shadingNode("multMatrix",au=True,name="%s_multMatrix"%parents)
        self.decomMatrix = cmds.shadingNode("decomposeMatrix",au=True,name="%s_decomposeMatrix"%parents)
        cmds.connectAttr(parents+".worldMatrix[0]",self.multMatrix+".matrixIn[0]")
        cmds.connectAttr(childs+".parentInverseMatrix[0]",self.multMatrix+".matrixIn[1]")
        cmds.connectAttr(self.multMatrix+".matrixSum",self.decomMatrix+".inputMatrix")
        if t == True:cmds.connectAttr(self.decomMatrix+".outputTranslate",childs+".translate")
        else:pass
        if r == True:cmds.connectAttr(self.decomMatrix+".outputRotate",childs+".rotate")
        else:pass
        if s == True:cmds.connectAttr(self.decomMatrix+".outputScale",childs+".scale")
        else:pass

        return [self.multMatrix, self.decomMatrix]

    #マトリックスコンストレイント専用。リグのコントローラーを作成し、色、大きさを変更
    #name : メソッド名 , CtlName　：　コントローラー名 , pcName : コンストレイントの親 , color : 色　, scale : スケール
    def createMatrixRigController(self,name,CtlName,pcName,color,scale):
        self.RigCtr = name("%s_Ctl"%CtlName)
        cmds.setAttr(self.RigCtr+".overrideEnabled",1)
        cmds.setAttr(self.RigCtr+".overrideColor",color)
        cmds.setAttr(self.RigCtr+".scale",scale,scale,scale)
        cmds.makeIdentity(self.RigCtr,apply=True,t=1,r=1,s=1)
        self.ctlOffsetGP = cmds.group(self.RigCtr,n="%s_Offset"%self.RigCtr)
        cmds.xform(self.ctlOffsetGP,piv=[0,0,0])
        self.pc = cmds.xform(pcName,q=True,ws=True,t=True)
        cmds.setAttr(self.ctlOffsetGP+".translate",*self.pc)
        #self.createChildAttrToParentGP(CtlName,self.RigCtr)
        return [self.ctlOffsetGP,self.RigCtr]

    #モジュール関連づけ用のヌルを作成
    def createModuleParentNull(self,parentName,childName):
        self.getPivot = cmds.xform(parentName,q=True,ws=True,rp=True)
        self.ConstraintGP = cmds.group(childName, n="Constraint_From__%s_Ctl"%parentName,r=True)
        cmds.xform(self.ConstraintGP,ws=True,piv = self.getPivot)

        return self.ConstraintGP

    #nodeに指定したジョイント階層を複製し、リネーム
    def dupRenameJoint(self,node,name):
        self.dupJointList = [] #複製しリネームしたジョイント階層名
        self.dup = cmds.duplicate(node,rc=True)
        for dups in self.dup:
            self.reName = cmds.rename(dups,"%s%s"%(name,dups.replace("1","")))
            self.dupJointList.append(self.reName)
        return self.dupJointList

    #リギング用の新しいジョイントを作成
    def createRiggingJoint(self,jointName,const,name):
        self.jointList = []
        #self.dagJoint = cmds.ls(jointName,dag=True,type="joint") #選択したジョイント階層をすべて取得
        cmds.select(d=True)
        for joints in jointName:
            self.pivot = cmds.xform(joints,q=True,ws=True,rp=True)
            self.jointSide = cmds.getAttr(joints+".side")#ジョイントのサイド
            self.jointType = cmds.getAttr(joints+".type")#ジョイントのタイプ

            self.joint = cmds.joint(p=self.pivot,n="%s_%s"%(name,joints))
            cmds.setAttr(self.joint+".side",self.jointSide)
            cmds.setAttr(self.joint+".type",self.jointType)
            self.jointList.append(self.joint)
            #cmds.parent(self.jointList[0],w=True)
            cmds.makeIdentity(self.joint,a=True,t=True,r=True,s=True,pn=True,jointOrient=True)
            if const == 0:pass
            elif const == 1:cmds.parentConstraint(self.joint,joints,mo=True)

        return self.jointList

    #Nurbsコントローラーの大きさを変更
    def setNurbsCtlScaling(self,ctl,valueX,valueY,valueZ):
        self.sel = cmds.ls(ctl)#,fl=True
        self.pp = []
        for sels in self.sel:
            self.spans = cmds.getAttr(self.sel[0]+".spans")
            for i in range(self.spans):
                self.point = cmds.pointPosition(sels+".cv[%d]"%i,l=True)
                self.pivot = cmds.xform(sels,q=True,ws=True,rp=True)
                self.point = [self.point[0]*valueX-self.pivot[0], self.point[1]*valueY-self.pivot[1], self.point[2]*valueZ-self.pivot[2]]
                cmds.xform(sels+".cv[%d]"%i,t=self.point)
