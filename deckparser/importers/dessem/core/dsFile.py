'''
Created on 12 de jul de 2018

@author: Renan
'''
import re

from .xmlReader import xmlReader

class dsFile:
    def __init__(self, cfg=None):
        self.records = {}
        self.tables = {}
        if 'xml' in cfg:
            self.loadConfig(cfg['xml'])
        else:
            raise ValueError('Need xml config file')
    
    def isEmpty(self):
        for k in self.records:
            if not self.records[k].isEmpty():
                return False
        for k in self.tables:
            if not self.tables[k].isEmpty():
                return False
        return True
    
    def openDSFile(self, fn):
        return open(fn, 'r')#, encoding='latin_1')
    
    def toDict(self, df=True):
        ds = {}
        for k in self.records:
            r = self.records[k]
            ds[k] = r.toDict(df)
        for k in self.tables:
            t = self.tables[k]
            ds[k] = t.toDict(df)
        return ds
    
    def loadConfig(self, fileName):
        xmlReader().decodeDsFile(self, fileName)
        
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
    
    def showData(self, showRaw=False, maxLines=None):
        for n in self.records:
            print('>> Record "{:s}"'.format(n))
            self.records[n].show(showRaw)
        for n in self.tables:
            print('>> Table "{:s}"'.format(n))
            self.tables[n].show(showRaw, maxLines)
    
    def showHeader(self):
        for n in self.records:
            print('>> Record "{:s}"'.format(n))
            self.records[n].showFields()
            print('-'*50)
        for n in self.tables:
            print('>> Table "{:s}"'.format(n))
            self.tables[n].showFields()
            print('-'*50)
    
    def test(self, fileName, maxLines=1e6):
        self.readDSFile(fileName)
        self.showData(showRaw=True, maxLines=maxLines)
    
    def listFields(self, reField, reRec):
        fields = dict()
        rl = self.listRecords(reRec)
        for n in rl:
            fl = rl[n].listFields(reField)
            for f in fl:
                if f not in fields:
                    fields[f] = [n]
                else:
                    fields[f].append(n)
        return fields
    
    def listRecords(self, reRec):
        pattern = re.compile(reRec)
        recs = dict()
        for rn in self.records:
            if pattern.match(rn) is not None:
                recs[rn] = self.records[rn]
        for rn in self.tables:
            if pattern.match(rn) is not None:
                recs[rn] = self.tables[rn]
        return recs
    