'''
Created on 12 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.xmlReader import xmlReader
import deckparser.importers.dessem.cfg as cfg

class dsFile:
    def __init__(self):
        self.records = {}
        self.tables = {}
        self.fileEncoding = None
        self.recFilter = None
        cfg = self.__getConfig()
        if 'xml' in cfg:
            self.loadConfig(cfg['xml'])
        else:
            raise ValueError('Missing xml config file')
    
    def isEmpty(self):
        for k in self.records:
            if not self.records[k].isEmpty():
                return False
        for k in self.tables:
            if not self.tables[k].isEmpty():
                return False
        return True
    
    def setEncoding(self, e):
        self.fileEncoding = e
    
    def openDSFile(self, fn):
        if self.fileEncoding:
            return open(fn, 'r', encoding=self.fileEncoding)
        return open(fn, 'r')
    
    def listRecords(self):
        r = []
        for n in self.records:
            r.append(n)
        for n in self.tables:
            r.append(n)
        return r
    
    def setRecFilter(self, recList):
        self.recFilter = recList
    
    def filterRec(self, r):
        if self.recFilter is None:
            return True
        if r in self.recFilter:
            return True
        return False
    
    def toDict(self, df=True):
        ds = {}
        for k in self.records:
            if not self.filterRec(k):
                continue
            r = self.records[k]
            ds[k] = r.toDict(df)
        for k in self.tables:
            if not self.filterRec(k):
                continue
            t = self.tables[k]
            ds[k] = t.toDict(df)
        return ds
    
    def getConfigPath(self):
        return cfg.__path__[0]
    
    def loadConfig(self, fileName):
        xmlReader(self.getConfigPath()).decodeDsFile(self, fileName)
        
    def addRec(self, name, r):
        self.records[name] = r
        
    def addTable(self, name, r):
        self.tables[name] = r
        
    def getRec(self, name):
        return self.records[name]
        
    def getTable(self, name):
        return self.tables[name]
    
    def clearData(self):
        for n in self.records:
            self.records[n].clear()
        for n in self.tables:
            self.tables[n].clear()
