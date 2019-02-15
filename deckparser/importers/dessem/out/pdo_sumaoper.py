import re
from datetime import date
from deckparser.importers.dessem.out.pdo_base_oper import pdo_base_oper, TableDef

class SumaTableDef(TableDef):
    def __init__(self, cs):
        super().__init__(cs)
    
    @staticmethod
    def balHidr():
        t = TableDef([5, 20, 26, 35, 45, 54, 63, 72, 80, 90, 99, 109, 115, 124],
                     ['i','s','f','f','f','f','f','f','f','f','f','f','f','f'],
                     ['idUhe', 'nome', 'volIniPerc', 'volIni', 'volAfl', 'volTurb', 'volVert', 'volDesv', 
                      'volDesc', 'volEvap', 'volAlt', 'volBomb', 'volFinalPerc', 'volFinal'],
                     [None, None, '%', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', '%', 'hm3'])
        return t
    
    @staticmethod
    def vazoes():
        t = TableDef([5, 22, 28, 38, 48, 58, 68, 78, 88, 98, 108, 118],
                     ['i','s','f','f','f','f','f','f','f','f','f','f'],
                     ['idUhe', 'nome', 'vazAfl', 'vazTurb', 'vazVert', 'vazDesv', 
                      'vazDesc', 'vazAlt', 'vazBomb', 'defMin', 'defMax', 'turbMax'],
                     [None, None, 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s'])
        return t
    
    @staticmethod
    def gerHidr():
        t = TableDef([5, 20, 24, 32, 42, 52, 62, 72, 82],
                     ['i','s','s','f','f','f','f','f','f'],
                     ['idUhe', 'nome', 'subSistema', 'vazTurb', 'gerHidr', 'reserv', 'gerMax', 'vt', 'produtibMed'],
                     [None, None, None, 'm3/s', 'MW', 'MW', 'MW', 'm3/s', 'MW/(m3/s)'])
        return t
    
    @staticmethod
    def custos():
        t = TableDef([41, 59],
                     ['s','f'],
                     ['descricao', 'valor'],
                     [None, None])
        return t

class pdo_sumaoper(pdo_base_oper):
    def __init__(self):
        super().__init__()
        self.addBlockType('day')
        self.addBlockType('week')
    
    def getTableSet(self):
        return {'1': SumaTableDef.balHidr(),
                 '2': SumaTableDef.vazoes(),
                 '3': SumaTableDef.gerHidr(),
                 '4': TableDef.gerTerm(),
                 '5a': TableDef.intercambioEnergetico(),
                 '5b': TableDef.intercambioEletrico(),
                 '6': TableDef.gerItaipu(),
                 '7': TableDef.energiaContratada(),
                 '8a': TableDef.balancoEnergetico(),
                 '8b': TableDef.balancoEletrico(),
                 '9': SumaTableDef.custos()}
    
    def checkOpenBlock_day(self, line):
        dtrex = '(\d{2})\/(\d{2})\/(\d{4})'
        rex = '\* RELATORIO FINAL DE OPERACAO NO DIA\s*(\d*) \: '+dtrex+'\s*\*'
        m = re.match(rex, line)
        if not m:
            return False
        d = int(m.group(1))
        dt = date(int(m.group(4)),
                  int(m.group(3)),
                  int(m.group(2)))
        self.setOpenBlock('day', d)
        self.setBlockIndex(dt.strftime('%Y-%m-%d'))
        return True
    
    def checkOpenBlock_week(self, line):
        rex = '\*  RELATORIO FINAL DE OPERACAO NA SEMANA (\d*)  \*'
        m = re.match(rex, line)
        if not m:
            return False
        w = int(m.group(1))
        self.setOpenBlock('week', w)
        return True
    
    def readWeekPeriod(self, line):
        dtrex = '(\d{2})\/(\d{2})\/(\d{4})'
        rex = '\*  PERIODO : '+dtrex+' a '+dtrex+'\s*\*'
        m = re.match(rex, line)
        if not m:
            return False
        dt1 = date(int(m.group(3)),
                   int(m.group(2)),
                   int(m.group(1)))
        dt2 = date(int(m.group(6)),
                   int(m.group(5)),
                   int(m.group(4)))
        dtf = '%Y-%m-%d'
        self.setBlockIndex([dt1.strftime(dtf), dt2.strftime(dtf)])
        return True
    
    def readFile(self, fileName):
        modo = None
        with self.openFile(fileName) as f:
            for line in f:
                ln = line.strip()
                if self.checkOpenBlock_day(ln):
                    modo = None
                elif self.checkOpenBlock_week(ln):
                    modo = 'week_period'
                elif self.checkOpenTable(ln):
                    if self.openTableKey == '9':
                        modo = 'data'
                    else:
                        modo = 'header'
                elif self.checkHeaderLimit(ln):
                    modo = 'data'
                elif modo == 'week_period':
                    if self.readWeekPeriod(line):
                        modo = None
                elif modo == 'header':
                    self.readHeaderLine(line)
                elif modo == 'data':
                    if self.checkEndOfTable(ln):
                        modo = None
                    else:
                        self.readDataLine(line)
        
        f.close()
    