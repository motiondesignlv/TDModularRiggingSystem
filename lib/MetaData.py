"メタノード作成"
import maya.cmds as cmds

class MetaData(object):
    #メタノード作成
    def createMetaNode(self,name):
        self.metaNode = cmds.createNode("network",n=name)
        
        return self.metaNode
    
    #文字列型のアトリビュートを追加
    def addStringAttribute(self,metaNode,attrName):
        cmds.addAttr(metaNode,ln=attrName,dt="string")
        cmds.setAttr(metaNode+"."+attrName,e=True,keyable=True)
        
        return metaNode+"."+attrName
    
    #文字列型のアトリビュートを編集
    def editStringAttribute(self,attrName,attrString):
        self.editString = cmds.setAttr(attrName,attrString,type="string")
        
        return attrString
    
    #float型のアトリビュートを追加
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
