'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.record import record


class table:
    
    def __init__(self, recMap):
        self.rec = record(recMap)
        self.clear()
        
    def isEmpty(self):
        return len(self.dataSet) == 0
     
    def toDict(self, df=True):
        fl = self.rec.listFields()
        lst = []
        ds = self.getData(df)
        for ln in ds:
            ds = {}
            for k in fl:
                ds[k] = ln.get(k)
            lst.append(ds)
        return lst
    
    def clear(self):
        self.dataSet = []
        self.metadataSet = []
        self.lineSet = []
        
    def addField(self, name, cfg):
        self.rec.addField(name, cfg)
        
    def setRange(self, key, r):
        self.rec.setRange(key, r)
        
    def setField(self, key, v):
        self.dataSet[len(self.dataSet)-1][key] = v
        
    def getDataDefault(self):
        ds = []
        for r in self.dataSet:
            ds.append(self.rec.applyDefault(r))
        return ds
        
    def applyDefault(self, r):
        return self.rec.applyDefault(r)
        
    def getData(self, applyDefault=True):
        if applyDefault:
            return self.getDataDefault()
        return self.dataSet
    
    def getField(self, key):
        return self.dataSet[len(self.dataSet)-1][key]
        
    def listFields(self, reField=None):
        return self.rec.listFields(reField)
    
    def showFields(self):
        return self.rec.showFields()
        
    def parseLine(self, line):
        r = self.rec.parse(line)
        self.dataSet.append(r)
        self.metadataSet.append(self.rec.metadata)
        self.lineSet.append(line)
        return r
    
    def show(self, showRaw=False, maxLines=None):
        ds = self.dataSet
        mds = self.normMetadata()
        
        n = len(ds)-1
        if maxLines:
            n = min(maxLines, n)
        
        for i in range(0, n):
            self.rec.showLine(ds[i], metadata=mds)
            if showRaw:
                print("R: " + self.lineSet[i])
    
    def normMetadata(self):
        ds = self.dataSet
        nmd = dict()
        
        for i in range(0, len(ds)-1):
            md = self.metadataSet[i]
            
            for k in md:
                if k not in nmd:
                    nmd[k] = md[k]
                    continue
                
                if 'format' in md[k]:
                    fk = 'format'
                    if 'format' in nmd[k]:
                        nmd[k][fk] = max(nmd[k][fk], md[k][fk])
                    else:
                        nmd[k][fk] = md[k][fk]
                        
                if 'just' in md[k] and 'just' not in nmd[k]:
                    nmd[k]['just'] = md[k]['just']
        return nmd