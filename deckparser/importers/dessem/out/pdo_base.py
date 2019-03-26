from deckparser.importers.dessem.out.pdo_common import parseValue
from deckparser.importers.dessem.out import cfg
import json
import os
import io

class ColumnDef:
    def __init__(self, f):
        self.name = f['name']
        self.type = f['type']
        self.unit = f.get('unit')
        self.desc = f.get('desc')
        self.short_desc = f.get('short_desc')

class TableDef:
    def __init__(self, fields):
        self.fields = fields
    
    def numOfCols(self):
        return len(self.fields)
    
    def searchColDef(self, nm):
        for f in self.fields:
            if f['name'] == nm:
                return ColumnDef(f)
    
    def getColDef(self, i):
        return ColumnDef(self.fields[i])

class pdo_base:
    def __init__(self, tableName):
        self.tableName = tableName
        self.tableDef = self.loadTableDef()
        self.data = []
    
    def loadTableDef(self):
        fPath = os.path.join(cfg.__path__[0], self.tableName+'.json')
        with io.open(fPath, 'r', encoding='utf8') as fp:
            d = json.load(fp, encoding='utf8')
        fp.close()
        return TableDef(d[self.tableName])
    
    def readHeaderLine(self, line):
        pass
    
    def readDataLine(self, line):
        rdt = self.splitLine(line)
        td = self.tableDef
        dt = {}
        for i in range(td.numOfCols()):
            cd = td.getColDef(i)
            dt[cd.name] = parseValue(rdt[i], cd.type)
        
        self.data.append(dt)
    
    def splitLine(self, line):
        dt = line.split(';')
        dt = [d.strip() for d in dt]
        return dt
    
    def checkHeaderLimit(self, ln):
        if ln == '':
            return False
        for c in ln:
            if c not in ['-', ';']:
                return False
        return True
    
    def openDSOFile(self, fn):
        return open(fn, 'r', encoding='iso-8859-1')
    
    def readFile(self, fileName):
        modo = None
        with self.openDSOFile(fileName) as f:
            for line in f.readlines():
                line = line.strip()
                if self.checkHeaderLimit(line):
                    if not modo:
                        modo = 'header'
                    elif modo == 'header':
                        modo = 'data'
                elif modo == 'header':
                    self.readHeaderLine(line)
                elif modo == 'data':
                    self.readDataLine(line)
        
        f.close()
    
    def export(self):
        return self.data
    