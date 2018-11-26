'''
Created on 7 de ago de 2018

@author: Renan Maciel
'''
import struct
import logging

class HIDR():
    def __init__(self):
        self.keyList = []
        self.lines = []
        self.recFilter = None
    
    def isEmpty(self):
        return len(self.lines) == 0
    
    def clearData(self):
        self.lines = []
        
    def listRecords(self):
        return ['UHE']
    
    def setRecFilter(self, recList):
        self.recFilter = recList
    
    def filterRec(self, r):
        if self.recFilter is None:
            return True
        if r in self.recFilter:
            return True
        return False
    
    def toDict(self):
        if not self.filterRec('UHE'):
            return {}
        lst = []
        for ln in self.lines:
            ds = {}
            for k in self.keyList:
                ds[k] = ln[k]
            lst.append(ds)
        return {'UHE': lst}
    
    def search(self, fileName, nomeUsina):
        c=1
        with open(fileName, 'rb') as f:
            while(self.readLine(f)):
                if self.currLine['nome'].find(nomeUsina) >= 0:
                    self.currLine['idUsina'] = c
                    self.lines.append(self.currLine)
                c=c+1
        f.close()
    
    def readDSFile(self, fileName, lines=1e6):
        c=1
        with open(fileName, 'rb') as f:
            while(self.readLine(f)):
                self.currLine['idUsina'] = c
                if self.currLine['idPosto'] > 0:
                    self.lines.append(self.currLine)
                c=c+1
                if c >= lines:
                    break
        f.close()
        
    def getField(self, k, default):
        f = self.currLine.get(k)
        if f is None: return default
        return f
        
    def readField(self, f, k, t, size):
        b = f.read(size)
        if b == '' or len(b)<size:
            return False
        try:
            self.currLine[k] = self.parseFieldValue(b, t)
        except struct.error as e:
            lg = logging.getLogger(__name__)
            lg.warning('HIDR: Parse exception: %s \nField: %s', str(e), k, exc_info=True)
            self.currLine[k] = None
            return False
        self.addKey(k)
        return True
    
    def addKey(self, k):
        if k not in self.keyList:
            self.keyList.append(k)
        
    def parseFieldValue(self, b, t):
        if t=='string':
            return b.decode('utf-8').strip()
        elif t=='int':
            return struct.unpack('i', b)[0]
        elif t=='real':
            return struct.unpack('f', b)[0]
        
        return None
    
    def readVector(self, f, k, t, n, size, limit=None):
        self.currLine[k] = self._readVector(f, t, n, size, limit)
        self.addKey(k)
        return True
    
    def _readVector(self, f, t, n, size, limit=None):
        v = []
        for i in range(0, n):
            b = f.read(size)
            if limit is None or i < limit:
                v.append(self.parseFieldValue(b, t))
        return v
    
    def readMultiVector(self, f, k, t, n, m, size, limit=None):
        mv = []
        for i in range(0, n):
            v = self._readVector(f, t, m, size)
            if limit is None or i < limit:
                mv.append(v)
        self.currLine[k] = mv
        self.addKey(k)
        return True
            
    def skip(self, f, s):
        f.read(s)
    
    def readLine(self, f):
        self.currLine = dict()
        self.shadowLine = dict()
        
        if not self.readField(f, 'nome', 'string', 12):
            return False
        self.readField(f, 'idPosto', 'int', 4)
        
        self.readField(f, 'idPostoBDH', 'string', 8)
        #self.skip(f, 8)
        
        self.readField(f, 'idSS', 'int', 4)
        self.skip(f, 4)
        self.readField(f, 'idUsinaJus', 'int', 4)
        self.readField(f, 'idUsinaJusDesvio', 'int', 4)
        self.readField(f, 'volMin', 'real', 4)
        self.readField(f, 'volMax', 'real', 4)
        self.readField(f, 'volSolVert', 'real', 4)
        self.readField(f, 'volSolDesvio', 'real', 4)
        self.skip(f, 8)
        
        self.readVector(f, 'polCotaVol', 'real', 5, 4)
        self.readVector(f, 'polAreaCota', 'real', 5, 4)
        self.readVector(f, 'coefEvap', 'int', 12, 4)
        self.readField(f, 'numCG', 'int', 4)
        numCG = self.getField('numCG', 5)
        self.readVector(f, 'numUG', 'int', 5, 4, limit=numCG)
        self.readVector(f, 'potencia', 'real', 5, 4, limit=numCG)

        # Trecho extraido do import do newave
        self.readMultiVector(f, 'Pol_QHT', 'real', 5, 5, 4, limit=numCG)
        self.readMultiVector(f, 'Pol_QHG', 'real', 5, 5, 4, limit=numCG)
        self.readMultiVector(f, 'Pol_PH', 'real', 5, 5, 4, limit=numCG)
        
        self.readVector(f, 'hef', 'real', 5, 4, limit=numCG)
        self.readVector(f, 'qef', 'int', 5, 4, limit=numCG)
        self.readField(f, 'prodEsp', 'real', 4)
        self.readField(f, 'perdaHidr', 'real', 4)
        
        self.readField(f, 'numCurvasCF', 'int', 4)
        numCF = self.getField('numCurvasCF', 6)
        self.readMultiVector(f, 'coefCF', 'real', 6, 5, 4, limit=numCF)
        self.readVector(f, 'cotaCF', 'real', 6, 4, limit=numCF)
        self.readField(f, 'cotaMediaCF', 'real', 4)
        self.readField(f, 'flagVertCF', 'int', 4)
        self.skip(f, 4*4)
        self.readField(f, 'tipoTurbina', 'int', 4)
        self.skip(f, 4)
        self.readField(f, 'teif', 'real', 4)
        self.readField(f, 'ip', 'real', 4)
        self.readField(f, 'tipoPerdasHidr', 'int', 4)
        self.readField(f, 'data', 'string', 8)
        self.readField(f, 'observacao', 'string', 43)
        self.readField(f, 'volRegula', 'real', 4)
        self.readField(f, 'tipoRegula', 'string', 1)
        
        return True
