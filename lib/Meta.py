"���^�m�[�h�쐬"
import maya.cmds as cmds

class MetaData(object):
    #���^�m�[�h�쐬
    def createMetaNode(self,name):
        self.metaNode = cmds.createNode("network",n=name)
        
        return self.metaNode
    
    #������^�̃A�g���r���[�g��ǉ�
    def addStringAttribute(self,metaNode,attrName):
        cmds.addAttr(metaNode,ln=attrName,dt="string")
        cmds.setAttr(metaNode+"."+attrName,e=True,keyable=True)
        
        return metaNode+"."+attrName
    
    #������^�̃A�g���r���[�g��ҏW
    def editStringAttribute(self,attrName,attrString):
        self.editString = cmds.setAttr(attrName,attrString,type="string")
        
        return attrString

sel = cmds.ls(sl=True)
meta = MetaData()
string = meta.addStringAttribute(sel[0],"t")
print meta.editStringAttribute(string,"aa")
