#-*- coding:utf-8 -*-
import maya.cmds as cmds
from TDModularRiggingSystem import RiggingSystem

#腕のリギング　【LR : 1=左、2=右】,【CtlColor : コントローラーの色】
class TDArmRigging():
    def __init__(self):
        #self.TDMRS.__init__()
        self.TDMRS  = RiggingSystem.ModularRiggingSystem()
        self.ArmNull = []#腕ジョイントのオフセットノード
        self.armRotateAttr = {}#デフォルトの腕ジョイントの回転値

    "-----コマンドの実行-----"
    def setArmRigging(self,LR,CtlColor,switchCtlName,ArmAttrList):
        TDArmRigging.getDefaultRotateAttr(self,LR)
        #TDArmRigging.createArmNull(self,LR)
        TDArmRigging.createFKArmJoint(self,LR,CtlColor)
        TDArmRigging.createIKArmJoint(self,LR,CtlColor)
        self.IKArmCtlList = TDArmRigging.createIKArmCtl(self,LR,CtlColor)
        TDArmRigging.createIKForeArmCtl(self,LR,CtlColor)
        TDArmRigging.createIKShoulderCtl(self,LR,CtlColor)
        TDArmRigging.createFKArmCtl(self,CtlColor)
        TDArmRigging.createIKArmExpression(self,LR,switchCtlName)
        self.ArmGrpList = TDArmRigging.setArmCtlLayering(self)
        TDArmRigging.setDefaultRotateAttr(self,LR)
        TDArmRigging.connectArmSwitch(self,LR,ArmAttrList)
        #TDArmRigging.addArmCtlClass(self,LR)

        return [self.IKArmCtlList, self.ArmGrpList]

    #デフォルトの回転値を保持し腕ジョイントをTポーズに戻す
    def getDefaultRotateAttr(self,LR):
        for armDRA in self.TDMRS.getBetweenJoint(self.TDMRS.getJointLabelType()[LR,9],self.TDMRS.getJointLabelType()[LR,12]):
            self.armRotateAttr[armDRA] = self.TDMRS.getJointRotate()[armDRA]
            cmds.setAttr(armDRA+".rotate",0,0,0)
    
    #腕ジョイントのオフセットノードを作成
    def createArmNull(self,LR):
        for armNulls in self.getBetweenJoint(self.getJointLabelType()[LR,9],self.getJointLabelType()[LR,12]):
            self.armNullGP = self.createGP(armNulls,"%s_Offset"%armNulls)
            self.ArmNull.append(self.armNullGP)

    #FKジョイントを作成
    def createFKArmJoint(self,LR,CtlColor):
        self.FKArmJoint = []
        if LR == 1:self.LeftRight = ["Left"]
        elif LR == 2:self.LeftRight = ["Right"]
        self.dupArmJointList = self.TDMRS.dupRenameJoint(self.TDMRS.getJointLabelType()[LR,9],"FK")
        for dupArmJointLists in reversed(self.dupArmJointList):
            if dupArmJointLists == "FK" + self.TDMRS.getJointLabelType()[LR,12]:
                cmds.parent(dupArmJointLists,self.TDMRS.getJointLabelType()[LR,9])
                self.FKArmJoint.append(dupArmJointLists)
            elif dupArmJointLists == "FK" + self.TDMRS.getJointLabelType()[LR,11]:
                cmds.parent(dupArmJointLists,self.TDMRS.getJointLabelType()[LR,9])
                self.FKArmJoint.append(dupArmJointLists)
            elif dupArmJointLists == "FK" + self.TDMRS.getJointLabelType()[LR,10]:
                self.FKArmJoint.append(dupArmJointLists)
            elif dupArmJointLists == "FK" + self.TDMRS.getJointLabelType()[LR,9]:
                self.FKArmJoint.append(dupArmJointLists)
            else:cmds.delete(dupArmJointLists)
        #reversed(self.FKArmJoint)
        cmds.parent(self.FKArmJoint[0],self.FKArmJoint[1])
        cmds.parent(self.FKArmJoint[1],self.FKArmJoint[2])

        self.FKArmJointOC     = cmds.orientConstraint(self.FKArmJoint[2],self.TDMRS.getJointLabelType()[LR,10],w=0,mo=True)
        self.FKForeArmJointOC = cmds.orientConstraint(self.FKArmJoint[1],self.TDMRS.getJointLabelType()[LR,11],w=0,mo=True)
        if LR == 1:
            self.FKHandJointOC    = cmds.orientConstraint(self.FKArmJoint[0],self.TDMRS.getJointLabelType()[LR,12],w=0,mo=True)
        elif LR == 2:
            self.FKHandJointOC    = cmds.orientConstraint(self.FKArmJoint[0],self.TDMRS.getJointLabelType()[LR,12],w=0,o=[180,0,0])
        self.FKShoulderJOffGP = self.TDMRS.createGP(self.FKArmJoint[-1],"%s_Offset"%self.FKArmJoint[-1])
        cmds.parent(self.FKShoulderJOffGP,w=True)
        #cmds.setAttr(self.FKArmOffGP+".visibility",0)

        """
        self.FKJoint = []#FKジョイントを取得
        if LR == 1:self.LeftRight = ["Left"]
        elif LR == 2:self.LeftRight = ["Right"]
        cmds.select(self.getJointLabelType()[LR,9])

        self.FKArmJ = cmds.joint(r=True,p=self.getJointWPosition(self.getJointLabelType()[LR,10]),n="FK%s"%self.getJointLabelType()[LR,10])
        self.FKForeArmJ = cmds.joint(r=True,p=self.getJointWPosition(self.getJointLabelType()[LR,11]),n="FK%s"%self.getJointLabelType()[LR,11])
        #cmds.setAttr(self.FKForeArmJ+".preferredAngleY",-90)
        self.pc = cmds.pointConstraint(self.getJointLabelType()[LR,11],self.FKForeArmJ)
        cmds.delete(self.pc)
        self.FKHandJ = cmds.joint(r=True,p=self.getJointWPosition(self.getJointLabelType()[LR,12]),n="FK%s"%self.getJointLabelType()[LR,12])
        self.pc = cmds.pointConstraint(self.getJointLabelType()[LR,12],self.FKHandJ)
        cmds.delete(self.pc)
        self.FKArmJointOC     = cmds.orientConstraint(self.FKArmJ,self.getJointLabelType()[LR,10],w=0,mo=True)
        self.FKForeArmJointOC = cmds.orientConstraint(self.FKForeArmJ,self.getJointLabelType()[LR,11],w=0,mo=True)
        self.FKHandJointOC    = cmds.orientConstraint(self.FKHandJ,self.getJointLabelType()[LR,12],w=0,mo=True)
        self.FKArmOffGP = self.createGP(self.FKArmJ,"%s_Offset"%self.FKArmJ)
        cmds.setAttr(self.FKArmOffGP+".visibility",0)
        """

    #IKジョイントを作成
    def createIKArmJoint(self,LR,CtlColor):
        cmds.select(self.TDMRS.getJointLabelType()[LR,9])
        self.IKArmJ = cmds.joint(r=True,p=self.TDMRS.getJointWPosition(self.TDMRS.getJointLabelType()[LR,10]),n="IK%s"%self.TDMRS.getJointLabelType()[LR,10])
        self.IKForeArmJ = cmds.joint(r=True,p=self.TDMRS.getJointWPosition(self.TDMRS.getJointLabelType()[LR,11]),n="IK%s"%self.TDMRS.getJointLabelType()[LR,11])
        cmds.setAttr(self.IKForeArmJ+".preferredAngleY",-90)
        self.pc = cmds.pointConstraint(self.TDMRS.getJointLabelType()[LR,11],self.IKForeArmJ)
        cmds.delete(self.pc)
        self.IKHandJ = cmds.joint(r=True,p=self.TDMRS.getJointWPosition(self.TDMRS.getJointLabelType()[LR,12]),n="IK%s"%self.TDMRS.getJointLabelType()[LR,12])
        self.pc = cmds.pointConstraint(self.TDMRS.getJointLabelType()[LR,12],self.IKHandJ)
        cmds.delete(self.pc)
        self.IKArmJointOC     = cmds.orientConstraint(self.IKArmJ,self.TDMRS.getJointLabelType()[LR,10],mo=True)
        self.IKForeArmJointOC = cmds.orientConstraint(self.IKForeArmJ,self.TDMRS.getJointLabelType()[LR,11],mo=True)
        if LR == 1:
            self.IKHandJointOC    = cmds.orientConstraint(self.IKHandJ,self.TDMRS.getJointLabelType()[LR,12],mo=True)
        elif LR == 2:
            self.IKHandJointOC    = cmds.orientConstraint(self.IKHandJ,self.TDMRS.getJointLabelType()[LR,12],o=[180,0,0])
        self.IKArmOffGP = self.TDMRS.createGP(self.IKArmJ,"%s_Offset"%self.IKArmJ)
        cmds.parentConstraint(self.TDMRS.getJointLabelType()[LR,9],self.IKArmOffGP,mo=True)
        cmds.setAttr(self.IKArmOffGP+".visibility",0)

    #IKのコントローラーの作成
    def createIKArmCtl(self,LR,CtlColor):
        self.armIK = cmds.ikHandle(sj = self.IKArmJ,ee = self.IKHandJ,
                                sol="ikRPsolver",name="%s_ikHandle"%self.TDMRS.getJointLabelType()[LR,12])
        self.armIKGP = self.TDMRS.createGP(self.armIK[0],"%s_GP"%self.armIK[0])
        cmds.setAttr(self.armIKGP+".visibility",0)
        #IKの手のコントローラー
        self.IKArmCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCube,self.IKHandJ,self.TDMRS.getJointLabelType()[LR,12],CtlColor,15)
        self.IKArmCtlPC = cmds.pointConstraint(self.IKArmCtl,self.TDMRS.gp)
        self.IKArmCtlOC = cmds.orientConstraint(self.IKArmCtl,self.IKHandJ,mo=True)
        self.IKArmCtlBlend = self.TDMRS.createGP(self.IKArmCtl,"%s_Blend"%self.IKArmCtl)

        return self.armIKGP

    #IKの肘のコントローラー
    def createIKForeArmCtl(self,LR,CtlColor):
        self.IKForeArmCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDsphere,self.IKForeArmJ,self.TDMRS.getJointLabelType()[LR,9],CtlColor,1)
        self.getPivot = cmds.xform(self.TDMRS.getJointLabelType()[LR,11],q=True,ws=True,rp=True)
        cmds.xform(self.IKForeArmCtl,ws=True,piv = self.getPivot)
        if LR == 1:cmds.setAttr(self.IKForeArmCtl+".rotateY",-90)
        else:cmds.setAttr(self.IKForeArmCtl+".rotateY",90)
        cmds.makeIdentity(self.IKForeArmCtl,apply=True,t=1,r=1,s=1)
        cmds.xform(self.IKForeArmCtl,cp=True)
        cmds.poleVectorConstraint(self.IKForeArmCtl,self.armIK[0],w=1)
        self.IKForeArmCtlBlend = self.TDMRS.createGP(self.IKForeArmCtl,"%s_Blend"%self.IKForeArmCtl)
        #cmds.aimConstraint(self.getJointLabelType()[LR,11],self.IKForeArmCtl,o=[0,90,0])

    #IKの鎖骨のコントローラー
    def createIKShoulderCtl(self,LR,CtlColor):
        self.shoulderCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCircle,self.TDMRS.getJointLabelType()[LR,9],self.TDMRS.getJointLabelType()[LR,9],CtlColor,15)
        if LR == 1:
            cmds.setAttr(self.shoulderCtl+".rotateZ",70)
        else:
            cmds.setAttr(self.shoulderCtl+".rotateZ",-70)
        cmds.makeIdentity(self.shoulderCtl,apply=True,t=1,r=1,s=1)
        self.shoulderCtlpp = cmds.parentConstraint(self.shoulderCtl,self.TDMRS.getJointLabelType()[LR,9],mo=True)
        self.shoulderCtlOffset = self.TDMRS.createGP(self.shoulderCtl,"%s_Offset"%self.shoulderCtl)

    #FKのコントローラーを作成
    def createFKArmCtl(self,CtlColor):
        "鎖骨のコントローラー"
        cmds.parent(self.shoulderCtlOffset,self.FKArmJoint[-1])
        cmds.makeIdentity(self.shoulderCtlOffset,apply=True,r=1)
        "肩のコントローラー"
        self.FKArmCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCircle,self.FKArmJoint[2],self.FKArmJoint[2],CtlColor,15)
        cmds.setAttr(self.FKArmCtl+".rotateZ",90)
        cmds.makeIdentity(self.FKArmCtl,apply=True,t=1,r=1,s=1)
        self.FKArmCtlBlend = self.TDMRS.createGP(self.FKArmCtl,"%s_Offset"%self.FKArmCtl)

        cmds.parent(self.FKArmCtlBlend,self.shoulderCtl)
        cmds.makeIdentity(self.FKArmCtlBlend,apply=True,r=1)

        self.FKArmJointRotate = self.TDMRS.createGP(self.FKArmCtlBlend,"%s_ArmJointRotate"%self.FKArmCtlBlend)
        self.FKArmGP = cmds.group(self.FKArmJointRotate,name="FK%sArm_GP"%self.LeftRight[0])

        cmds.parent(self.FKArmJoint[2],self.FKArmCtl)
        cmds.makeIdentity(self.FKArmCtl,apply=True,r=1)
        #self.FKArmCtlop = cmds.orientConstraint(self.FKArmCtl,self.FKArmJoint[2],mo=True)
        "肘のコントローラー"
        self.FKForeArmCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCircle,self.FKArmJoint[1],self.FKArmJoint[1],CtlColor,15)
        cmds.setAttr(self.FKForeArmCtl+".rotateZ",90)
        cmds.makeIdentity(self.FKForeArmCtl,apply=True,t=1,r=1,s=1)
        self.FKForeArmCtlBlend = self.TDMRS.createGP(self.FKForeArmCtl,"%s_Offset"%self.FKForeArmCtl)

        cmds.parent(self.FKForeArmCtlBlend,self.FKArmJoint[2])
        cmds.makeIdentity(self.FKForeArmCtlBlend,apply=True,r=1)
        cmds.parent(self.FKArmJoint[1],self.FKForeArmCtl)
        #self.FKForeArmCtlop = cmds.orientConstraint(self.FKForeArmCtl,self.FKArmJoint[1],mo=True)
        "手のコントローラー"
        self.FKHandCtl = self.TDMRS.createRigController(self.TDMRS.TDcrc.TDCircle,self.FKArmJoint[0],self.FKArmJoint[0],CtlColor,15)
        self.IKArmCtlOCAttr = cmds.getAttr(self.IKArmCtlOC[0]+".offset")
        cmds.setAttr(self.FKHandCtl+".rotateZ",90)
        self.FKHandCtlBlend = self.TDMRS.createGP(self.FKHandCtl,"%s_Offset"%self.FKHandCtl)

        cmds.parent(self.FKHandCtlBlend,self.FKArmJoint[1])
        cmds.makeIdentity(self.FKHandCtl,apply=True,t=1,r=1,s=1)
        cmds.parent(self.FKArmJoint[0],self.FKHandCtl)
        #cmds.makeIdentity(self.FKHandCtl,apply=True,r=1)
        #self.FKHandCtlop = cmds.orientConstraint(self.FKHandCtl,self.FKArmJoint[0],o=self.IKArmCtlOCAttr[0])
        "オフセットヌルの作成"
        cmds.makeIdentity(self.FKArmCtl,apply=True,r=1)

        "FKジョイントとコントローラーの階層化"

        "手首FKのワールド回転値を保持するロケータ"
        self.FKHandRotLoc = cmds.spaceLocator(n="%s_RotateLocator"%self.FKHandCtl)
        self.pc = cmds.pointConstraint(self.FKHandCtl,self.FKHandRotLoc)
        cmds.delete(self.pc)
        cmds.parentConstraint(self.FKHandCtl,self.FKHandRotLoc)

    #シームレスなFKIKスイッチエクスプレッションを作成
    def createIKArmExpression(self,LR,switchCtlName):
        if LR == 1:LR = "Left"
        elif LR == 2:LR = "Right"
        if LR == "Left":
            self.ArmExpression = cmds.expression(n="%sFKArm_Expression"%LR,ae=0,\
                s=u'/*値をコネクト*/\n'
                +'undoInfo -ock;\n'
                +'%s.%sW1 = %s.%sArm_IK_FK;\n'%(self.IKArmJointOC[0],self.IKArmJ,switchCtlName,LR)
                +'%s.%sW1 = %s.%sArm_IK_FK;\n'%(self.IKForeArmJointOC[0],self.IKForeArmJ,switchCtlName,LR)
                +'%s.%sW1 = %s.%sArm_IK_FK;\n\n'%(self.IKHandJointOC[0],self.IKHandJ,switchCtlName,LR)

                +'if(%s.%sArm_IK_FK == 1){\n'%(switchCtlName,LR)
                +u'/*ジョイントのベクトル値を取得*/\n'
                +'vector $FKWpos = `xform -q -ws -t %s`;\n'%self.FKArmJoint[0]
                +'vector $FKEpos = `xform -q -ws -t %s`;\n'%self.FKArmJoint[1]
                +'vector $FKSpos = `xform -q -ws -t %s`;\n'%self.FKArmJoint[2]
                +'vector $IKHand = `xform -q -ws -rp %s`;\n'%self.IKArmCtlBlend
                +'vector $IKForeArm = `xform -q -ws -rp %s`;\n'%self.IKForeArmCtlBlend
                +'vector $FKWrot = `getAttr "%s.rotate"`;\n'%self.FKHandCtl
                +'vector $IKHandPos = $FKWpos - $IKHand;\n\n'

                +u'/*手のIKコントローラーを手のFKジョイントの位置に移動*/\n'
                +'setAttr "%s.translate" ($IKHandPos.x)($IKHandPos.y)($IKHandPos.z);\n'%self.IKArmCtl
                +'//string $pointC[] = `pointConstraint %s %s`;\n'%(self.FKArmJoint[0],self.IKArmCtl)
                +'//string $orientC[] = `orientConstraint %s %s`;\n'%(self.FKArmJoint[0],self.IKArmCtl)
                +'vector $IKHandRot = `getAttr "%s.rotate"`;\n'%self.FKHandRotLoc[0]
                +'//delete $orientC;\n'
                +'setAttr "%s.rotate" ($IKHandRot.x)($IKHandRot.y)($IKHandRot.z);\n\n'%self.IKArmCtl

                +u'/*ベクトルの計算*/\n'
                +'vector $midp = ($FKWpos + $FKSpos)/2;\n'
                +'vector $PVpos = $FKEpos - $midp;\n'
                +'vector $polePos = 5*$PVpos + $midp;\n'
                +'vector $IKForeArmPos = $polePos - $IKForeArm;\n\n'

                +u'/*肘のIKコントローラーを計算したベクトル位置に移動*/\n'
                +'setAttr "%s.translate" ($IKForeArmPos.x)($IKForeArmPos.y)($IKForeArmPos.z);\n'%self.IKForeArmCtl
                #+'select %s;\n'%self.SwitchCtl
                +'}\n\n'

                +'else if(%s.%sArm_IK_FK == 0){\n'%(switchCtlName,LR)
                +'vector $IKWpos = `getAttr "%s.rotate"`;\n'%self.IKHandJ
                +'vector $IKEpos = `getAttr "%s.rotate"`;\n'%self.IKForeArmJ
                +'vector $IKSpos = `getAttr "%s.rotate"`;\n'%self.IKArmJ
                +'vector $ArmJointRotate = `getAttr "%s.rotate"`;\n\n'%self.FKArmJointRotate

                +'setAttr "%s.rotate" ($IKSpos.x - $ArmJointRotate.x)($IKSpos.y - $ArmJointRotate.y)($IKSpos.z - $ArmJointRotate.z);\n'%self.FKArmCtl
                +'setAttr "%s.rotate" ($IKEpos.x)($IKEpos.y)($IKEpos.z);\n'%self.FKForeArmCtl
                +'setAttr "%s.rotate" ($IKWpos.x)($IKWpos.y)($IKWpos.z);\n'%self.FKHandCtl
                +'}\n'
                +'undoInfo -cck;\n')
        elif LR == "Right":
            self.ArmExpression = cmds.expression(n="%sFKArm_Expression"%LR,ae=0,\
                s=u'/*値をコネクト*/\n'
                +'undoInfo -ock;\n'
                +'%s.%sW1 = %s.%sArm_IK_FK;\n'%(self.IKArmJointOC[0],self.IKArmJ,switchCtlName,LR)
                +'%s.%sW1 = %s.%sArm_IK_FK;\n'%(self.IKForeArmJointOC[0],self.IKForeArmJ,switchCtlName,LR)
                +'%s.%sW1 = %s.%sArm_IK_FK;\n\n'%(self.IKHandJointOC[0],self.IKHandJ,switchCtlName,LR)

                +'if(%s.%sArm_IK_FK == 1){\n'%(switchCtlName,LR)
                +u'/*ジョイントのベクトル値を取得*/\n'
                +'vector $FKWpos = `xform -q -ws -t %s`;\n'%self.FKArmJoint[0]
                +'vector $FKEpos = `xform -q -ws -t %s`;\n'%self.FKArmJoint[1]
                +'vector $FKSpos = `xform -q -ws -t %s`;\n'%self.FKArmJoint[2]
                +'vector $IKHand = `xform -q -ws -rp %s`;\n'%self.IKArmCtlBlend
                +'vector $IKForeArm = `xform -q -ws -rp %s`;\n'%self.IKForeArmCtlBlend
                +'vector $FKWrot = `getAttr "%s.rotate"`;\n'%self.FKHandCtl
                +'vector $IKHandPos = $FKWpos - $IKHand;\n\n'

                +u'/*手のIKコントローラーを手のFKジョイントの位置に移動*/\n'
                +'setAttr "%s.translate" ($IKHandPos.x)($IKHandPos.y)($IKHandPos.z);\n'%self.IKArmCtl
                +'//string $pointC[] = `pointConstraint %s %s`;\n'%(self.FKArmJoint[0],self.IKArmCtl)
                +'//string $orientC[] = `orientConstraint %s %s`;\n'%(self.FKArmJoint[0],self.IKArmCtl)
                +'vector $IKHandRot = `getAttr "%s.rotate"`;\n'%self.FKHandRotLoc[0]
                +'//delete $orientC;\n'
                +'setAttr "%s.rotate" ($IKHandRot.x)($IKHandRot.y)($IKHandRot.z);\n\n'%self.IKArmCtl

                +u'/*ベクトルの計算*/\n'
                +'vector $midp = ($FKWpos + $FKSpos)/2;\n'
                +'vector $PVpos = $FKEpos - $midp;\n'
                +'vector $polePos = 5*$PVpos + $midp;\n'
                +'vector $IKForeArmPos = $polePos - $IKForeArm;\n\n'

                +u'/*肘のIKコントローラーを計算したベクトル位置に移動*/\n'
                +'setAttr "%s.translate" ($IKForeArmPos.x)($IKForeArmPos.y)($IKForeArmPos.z);\n'%self.IKForeArmCtl
                #+'select %s;\n'%self.SwitchCtl
                +'}\n\n'

                +'else if(%s.%sArm_IK_FK == 0){\n'%(switchCtlName,LR)
                +'vector $IKWpos = `getAttr "%s.rotate"`;\n'%self.IKHandJ
                +'vector $IKEpos = `getAttr "%s.rotate"`;\n'%self.IKForeArmJ
                +'vector $IKSpos = `getAttr "%s.rotate"`;\n'%self.IKArmJ
                +'vector $ArmJointRotate = `getAttr "%s.rotate"`;\n\n'%self.FKArmJointRotate

                +'setAttr "%s.rotate" ($IKSpos.x - $ArmJointRotate.x)(($IKSpos.y - $ArmJointRotate.y)* -1)(($IKSpos.z - $ArmJointRotate.z)* -1);\n'%self.FKArmCtl
                +'setAttr "%s.rotate" ($IKEpos.x)($IKEpos.y * -1)($IKEpos.z * -1);\n'%self.FKForeArmCtl
                +'setAttr "%s.rotate" ($IKWpos.x)($IKWpos.y * -1)($IKWpos.z * -1);\n'%self.FKHandCtl
                +'}\n'
                +'undoInfo -cck;\n')
        cmds.setAttr(self.IKForeArmCtl+".translate",0,0,0)

    #腕のコントローラーの階層分け
    def setArmCtlLayering(self):
        self.IKArmGP = cmds.group(self.IKForeArmCtlBlend,self.IKArmCtlBlend,name="IK%sArm_GP"%self.LeftRight[0])
        self.IKArmJointRotate = cmds.group(self.IKForeArmCtlBlend,self.IKArmCtlBlend,name="IK%sArm_ArmJointRotate"%self.LeftRight[0])
        self.ArmGP = cmds.group(self.FKShoulderJOffGP,name="%sArm_GP"%self.LeftRight[0])
        cmds.xform(self.ArmGP,ws=True,piv = cmds.xform(self.FKArmJoint[-1],q=True,ws=True,rp=True))

        #cmds.makeIdentity(self.shoulderCtlOffset,apply=True,r=True)
        cmds.parent(self.IKArmGP,self.ArmGP)

        return self.ArmGP

    #腕のデフォルト回転値をセット
    def setDefaultRotateAttr(self,LR):
        self.getShoulderPivot = cmds.xform(self.TDMRS.getJointLabelType()[LR,10],q=True,ws=True,rp=True)
        cmds.xform(self.IKArmJointRotate,ws=True,piv = self.getShoulderPivot)
        cmds.setAttr(self.IKArmJointRotate+".rotate",*self.armRotateAttr[self.TDMRS.getJointLabelType()[LR,10]])
        cmds.setAttr(self.FKArmJointRotate+".rotate",*self.armRotateAttr[self.TDMRS.getJointLabelType()[LR,10]])

    #腕のFKIKスイッチコネクション
    def connectArmSwitch(self,LR,ArmAttrList):
        if LR == 1:self.LeftRight = ArmAttrList
        elif LR == 2:self.LeftRight = ArmAttrList
        "肩のスイッチング"
        self.reverse = cmds.shadingNode("reverse",au=True,n="%s_reverse"%self.FKArmJoint[2])
        #cmds.connectAttr(self.LeftRight,self.IKArmJointOC[0]+".%sW1"%self.IKArmJ,f=True)
        cmds.connectAttr(self.LeftRight,self.reverse+".inputX",f=True)
        cmds.connectAttr(self.reverse+".outputX",self.FKArmJointOC[0]+".%sW0"%self.FKArmJoint[2],f=True)
        "肘のスイッチング"
        #cmds.connectAttr(self.LeftRight,self.IKForeArmJointOC[0]+".%sW1"%self.IKForeArmJ,f=True)
        cmds.connectAttr(self.reverse+".outputX",self.FKForeArmJointOC[0]+".%sW0"%self.FKArmJoint[1],f=True)
        "手のスイッチング"
        #cmds.connectAttr(self.LeftRight,self.IKHandJointOC[0]+".%sW1"%self.IKHandJ,f=True)
        cmds.connectAttr(self.reverse+".outputX",self.FKHandJointOC[0]+".%sW0"%self.FKArmJoint[0],f=True)

        cmds.connectAttr(self.LeftRight,self.IKArmGP+".visibility",f=True)
        cmds.connectAttr(self.reverse+".outputX",self.FKArmGP+".visibility",f=True)

    #階層クラスに腕コントローラー
    def addArmCtlClass(self,LR):
        if LR == 1: TDCtlLayering.LeftArmIKGP = self.armIKGP
        elif LR == 2:TDCtlLayering.RightArmIKGP = self.armIKGP
        if LR == 1: TDCtlLayering.LeftArmGP = self.ArmGP
        elif LR == 2:TDCtlLayering.RightArmGP = self.ArmGP
