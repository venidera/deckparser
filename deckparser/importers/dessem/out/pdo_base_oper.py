import re
from deckparser.importers.dessem.out.pdo_common import parseValue

class ColumnDef:
    def __init__(self, ce, cf, cn):
        self.colEnd = ce
        self.colFormat = cf
        self.colName = cn

class TableDef:
    def __init__(self, cs, cf, cn, unt):
        self.colSpacing = cs
        self.colFormat = cf
        self.colName = cn
        self.colUnit = unt
    
    def numOfCols(self):
        return len(self.colSpacing)
    
    def getColDef(self, i):
        return ColumnDef(self.colSpacing[i],
                         self.colFormat[i],
                         self.colName[i])
    
    def getUnitDict(self):
        unt = {}
        for i in range(self.numOfCols()):
            unt[self.colName[i]] = self.colUnit[i]
        return unt
    
    @staticmethod
    def gerTerm():
        t = TableDef([5, 21, 25, 33, 43, 53, 63, 73],
                     ['i','s','s','f','f','f','f','f'],
                     ['idUte', 'nome', 'idSubsistema', 'gerMin', 'gerTerm', 'reserv', 'gerMax', 'capacidade'],
                     [None, None, None, 'MW', 'MW', 'MW', 'MW', 'MW'])
        return t
    
    @staticmethod
    def intercambioEnergetico():
        t = TableDef([7, 12, 19, 29],
                     ['s','s','f','f'],
                     ['orig', 'dest', 'intercambio', 'intercMax'],
                     [None, None, 'MW', 'MW'])
        return t

    @staticmethod
    def intercambioEletrico():
        t = TableDef([7, 12, 19, 29],
                     ['s','s','f','f'],
                     ['orig', 'dest', 'intercambio', 'intercMax'],
                     [None, None, 'MW', 'MW'])
        return t

    @staticmethod
    def gerItaipu():
        t = TableDef([10, 23, 36],
                     ['f','f','f'],
                     ['ger60Hz', 'ger50HzSE', 'ger50HzANDE'],
                     ['MW', 'MW', 'MW'])
        return t
    
    @staticmethod
    def energiaContratada():
        t = TableDef([15, 23, 28, 35, 45, 55, 65],
                     ['s','s','s','f','f','f','f'],
                     ['nomeContrato', 'tipoContrato', 'idSubsistema', 'qtdMin', 'qtdContr', 'qtdMax', 'custo'],
                     [None, None, None, 'MW', 'MW', 'MW', '$/MWh'])
        return t
    
    @staticmethod
    def balancoEnergetico():
        t = TableDef([6, 13, 22, 31, 40, 49, 58, 67, 76, 85, 94, 103, 110, 119, 127, 135, 144, 153, 164, 171],
                     ['s','f','f','f','f','f','f','f','f','f','f','f','f','f','s','f','f','f','f','f'],
                     ['siglaSubsistema', 'cmo', 'demanda', 'perdas', 'gerPeq', 'gerFixBar', 'gerHidr', 'gerTerm', 
                      'consue', 'importacao', 'exportacao', 'deficit', 'deficitPerc', 'saldo', 'observacao', 
                      'gerTermMin', 'impMin', 'expMin', 'earmFinal', 'earmFinalPerc'],
                     [None, '$/MWh', 'MW', 'MW', 'MW', 'MW', 'MW', 'MW', None, 'MW', 'MW', 'MW', '%', 'MW', None, 'MW', 'MW', 'MW', 'MWmes', '%'])
        return t
    
    @staticmethod
    def balancoEletrico():
        t = TableDef([9, 18, 27, 40, 51],
                     ['s','f','f','f','f'],
                     ['siglaSubsistema', 'demanda', 'perdas', 'geracao', 'saldo'],
                     [None, 'MW', 'MW', 'MW', 'MW'])
        return t

class pdo_base_oper:
    def __init__(self):
        self.tableSet = self.getTableSet()
        self.blockGroup = {}
        self.blockIndex = {}
        self.openBlock = None
        self.openTableKey = None
    
    def openFile(self, fn):
        return open(fn, 'r')
    
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
        ci = 1
        for i in range(td.numOfCols()):
            cdef = td.getColDef(i)
            cd = cdef.colEnd
            cf = cdef.colFormat
            rv = line[(ci-1):(cd-1)]
            try:
                v = parseValue(rv, cf)
            except ValueError:
                print('Field range: ({:d}, {:d})'.format(ci, cd))
                print('Value: '+rv)
                raise
            ci = cd
            lnd[cdef.colName] = v
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
    