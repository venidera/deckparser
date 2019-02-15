from deckparser.importers.dessem.out.pdo_common import parseValue

class ColumnDef:
    def __init__(self, cn, cf):
        self.colName = cn
        self.colFormat = cf

class TableDef:
    def __init__(self, cn, cf, unt):
        self.colName = cn
        self.colFormat = cf
        self.colUnit = unt
    
    def numOfCols(self):
        return len(self.colName)
    
    def getColDef(self, i):
        return ColumnDef(self.colName[i],
                         self.colFormat[i])

class pdo_base:
    def __init__(self):
        self.tableDef = self.getTableDef()
        self.data = []
    
    def readHeaderLine(self, line):
        pass
    
    def readDataLine(self, line):
        rdt = self.splitLine(line)
        td = self.tableDef
        dt = {}
        for i in range(td.numOfCols()):
            cd = td.getColDef(i)
            dt[cd.colName] = parseValue(rdt[i], cd.colFormat)
        
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
        return open(fn, 'r')
    
    def readFile(self, fileName):
        modo = None
        with self.openDSOFile(fileName) as f:
            for line in f:
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
    