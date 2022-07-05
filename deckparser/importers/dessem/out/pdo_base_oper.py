import re
from deckparser.importers.dessem.out.pdo_common import parseValue
import os
import json
from deckparser.importers.dessem.out import cfg
from deckparser.importers.dessem.out.cfg import modif as cfg_modif
import io
import logging

class ColumnDef:
    def __init__(self, f):
        self.range = [f['c'], f['cf']]
        self.type = f['type']
        self.name = f['name']
        self.unit = f.get('unit')
        self.desc = f.get('desc')
        self.short_desc = f.get('short_desc')

class TableDef:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    
    def numOfCols(self):
        return len(self.fields)
    
    def searchColDef(self, nm):
        for f in self.fields:
            if f['name'] == nm:
                return ColumnDef(f)
    
    def getColDef(self, i):
        return ColumnDef(self.fields[i])
    
    def getUnitDict(self):
        unt = {}
        for i in range(self.numOfCols()):
            cd = self.getColDef(i)
            unt[cd.name] = cd.unit
        return unt

class pdo_base_oper:
    def __init__(self, tableName):
        self.tableName = tableName
        self.tableSet = self.loadTableSet()
        self.blockGroup = {}
        self.blockIndex = {}
        self.openBlock = None
        self.openTableKey = None
    
    def loadTableSet(self):
        fPath = os.path.join(cfg.__path__[0], self.tableName+'.json')
        with io.open(fPath, 'r', encoding='utf8') as fp:
            try:
                d = json.load(fp, encoding='utf8')
            except:
                # editado pela thayze
                with open(fPath, encoding='utf8') as f:
                    d = json.load(f)
        
        #with open(os.path.join(cfg.__path__[0], self.tableName+'.json'), 'r') as fp:
        #    d = json.load(fp, encoding='utf-8')
        fp.close()
        ts = {}
        for tk,td in d.items():
            ts[tk] = TableDef(td['name'], td['fields'])
        return ts
    
    def applyModif(self, dessem_version):
        tableModif = self.loadTableModif(dessem_version)
        v_sorted = list(sorted(tableModif.keys()))
        for v in v_sorted:
            for tk,td in tableModif[v].items():
                self.getLogger().info('Table {:s} - {:s} structure modification applied (from vesion: {:s})'.
                                      format(tk, td.name, str(v)))
                self.tableSet[tk] = td
    
    def loadTableModif(self, dessem_version):
        mdPath = cfg_modif.__path__[0]
        ts_modif = {}
        for fn in os.listdir(mdPath):
            rex = '([0-9]{1,2})_([0-9]{1,2})\.json'
            m = re.match(rex, fn)
            if not m:
                continue
            md_version = (int(m.group(1)),int(m.group(2)))
            if self.compare_version(md_version, dessem_version) > 0:
                continue

            fPath = os.path.join(mdPath, fn)
            with io.open(fPath, 'r', encoding='utf8') as fp:
                try:
                    d = json.load(fp, encoding='utf8')
                except:
                    # editado pela thayze
                    with open(fPath, encoding='utf8') as fptemp:
                        d = json.load(fptemp)

            fp.close()
            d_pdo_op = d.get(self.tableName)
            if not d_pdo_op:
                continue
            ts = {}
            for tk,td in d_pdo_op.items():
                ts[tk] = TableDef(td['name'], td['fields'])
            ts_modif[md_version] = ts
        return ts_modif
    
    def compare_version(self, v1, v2, level=0):
        if level >= min(len(v1),len(v2)):
            return 0
        lv1 = v1[level]
        lv2 = v2[level]
        if lv1 > lv2:
            return 1
        if lv1 == lv2:
            return self.compare_version(v1, v2, level+1)
        return -1
    
    def openFile(self, fn):
        return open(fn, 'r', encoding='iso-8859-1')
    
    def getTableDef(self, k):
        return self.tableSet.get(k)
    
    def addBlockType(self, tp):
        self.blockGroup[tp] = {}
        self.blockIndex[tp] = {}
    
    def setBlockIndex(self, idxVal):
        tp = self.openBlock['type']
        k = self.openBlock['key']
        self.blockIndex[tp][k] = idxVal
    
    def setOpenBlock(self, blockType, k):
        self.openBlock = {'type': blockType, 'key': k}
    
    def getBlock(self, tp):
        return self.blockGroup[tp]
        
    def getOpenBlock(self):
        tp = self.openBlock['type']
        k = self.openBlock['key']
        b = self.blockGroup[tp]
        if k not in b:
            b[k] = {}
        return b[k]
    
    def getOpenTable(self):
        return self.getOpenBlock()[self.openTableKey]
    
    def checkOpenTable(self, line):
        rex = '(\d*[a-zA-Z]?) - (.*)\:?'
        m = re.match(rex, line)
        if not m:
            return False
        tableKey = m.group(1)
        tableCaption = self.parseTableCaption(m.group(2))
        
        b = self.getOpenBlock()
        try:
            tableUnits = self.getTableDef(tableKey).getUnitDict()
        except AttributeError:
            print(tableKey)
            raise
        b[tableKey] = {'caption': tableCaption, 'units': tableUnits}
        self.openTableKey = tableKey
        return True
    
    def parseTableCaption(self, c):
        us = c.rfind('(')
        ue = c.rfind(')')
        if us >= 0 and ue >= 0:
            return {'title': c[:us].strip(), 'unit': c[us+1:ue]}
        return {'title': c, 'unit': None}
    
    def checkHeaderLimit(self, ln):
        if ln == '':
            return False
        n = min(len(ln),10)
        for c in ln[0:n]:
            if c != '-':
                return False
        return True
    
    def readHeaderLine(self, line):
        pass
    
    def readDataLine(self, line):
        if line.strip() != '':
            ot = self.getOpenTable()
            if 'data' not in ot:
                ot['data'] = []
            try:
                ot['data'].append(self.parseDataLine(line))
            except ValueError:
                print('Line: '+line)
                raise
    
    def parseHeaderLine(self, line):
        return line.split()
    
    def parseDataLine(self, line):
        td = self.getTableDef(self.openTableKey)
        if not td:
            return line
        
        lnd = {}
        for i in range(td.numOfCols()):
            cdef = td.getColDef(i)
            r = cdef.range
            rv = line[r[0]:r[1]]
            try:
                v = parseValue(rv, cdef.type)
            except ValueError:
                print('Field range: ({:d}, {:d})'.format(r[0], r[1]))
                print('Value: '+rv)
                raise
            lnd[cdef.name] = v
        return lnd
    
    def checkEndOfTable(self, line):
        if line == '':
            return True
        if self.checkEndOfBlock(line):
            return True
        return False
    
    def checkEndOfBlock(self, line):
        for c in line:
            if c != '=':
                return False
        return True
    
    def export(self):
        e = {}
        for k,b in self.blockIndex.items():
            e[k+'_index'] = b
        for k,b in self.blockGroup.items():
            e[k+'_data'] = b
        return e
    
    def getLogger(self):
        return logging.getLogger(__name__)
    