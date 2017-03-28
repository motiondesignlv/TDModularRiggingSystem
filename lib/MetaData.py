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
    
    #float�^�̃A�g���r���[�g��ǉ�
    def addFloatAttribute(self,metaNode,attrName):
        cmds.addAttr(metaNode,ln=attrName,at="double")
        cmds.setAttr(metaNode+"."+attrName,e=True,keyable=True)
        
        return metaNode+"."+attrName
        

#sel = cmds.ls(sl=True)
meta = MetaData()
node = meta.createMetaNode("metaNode")
string = meta.addStringAttribute(node,"childMetaData")
meta.editStringAttribute(string,"test")
meta.addFloatAttribute(node,"testFloat")
