import re
from datetime import datetime
from deckparser.importers.dessem.out.pdo_base_oper import pdo_base_oper, TableDef

class OperTableDef(TableDef):
    def __init__(self, cs):
        super().__init__(cs)
    
    @staticmethod
    def balHidr():
        t = TableDef([5, 20, 23, 29, 39, 48, 57, 66, 75, 84, 93, 102, 111, 120, 129, 136, 147],
                     ['i','s','s','f','f','f','f','f','f','f','f','f','f','f','f','f','f'],
                     ['idUhe', 'nome', 'subSistema', 'volIniPerc', 'volIni', 'volIncr', 
                      'volMontV', 'volMont', 'volTurb', 'volVert', 'volDesv', 'volDesc', 
                      'volEvap', 'volAlt', 'volBomb', 'volFinalPerc', 'volFinal'],
                     [None, None, None, '%', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', 
                      'hm3', 'hm3', 'hm3', 'hm3', 'hm3', 'hm3', '%', 'hm3'])
        return t
    
    @staticmethod
    def vazoes():
        t = TableDef([5, 20, 23, 31, 44, 53, 62, 71, 80, 89, 98, 107, 116, 125],
                     ['i','s','s','f','f','f','f','f','f','f','f','f','f','f'],
                     ['idUhe', 'nome', 'subSistema', 'vazIncr', 'vazMontV', 'vazMont', 
                      'vazTurb', 'vazVert', 'vazDesv', 'vazDesc', 'vazAlt', 'vazBomb', 'defMin', 'defMax'],
                     [None, None, None, 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s', 'm3/s'])
        return t
    
    @staticmethod
    def gerHidr():
        t = TableDef([4, 19, 22, 30, 39, 48, 57, 66, 75, 84, 91, 100],
                     ['i','s','s','f','f','f','f','f','f','f','f','f'],
                     ['idUhe', 'nome', 'subSistema', 'vazTurb', 'vazTurbMax', 
                      'gerHidr', 'reserv', 'gerMax', 'vt', 'valorAgua', 'altQueda', 'produtib'],
                     [None, None, None, 'm3/s', 'm3/s', 'MW', 'MW', 'MW', 'm3/s', '$/MWh', 'm', 'MW/(m3/s)'])
        return t
    
    @staticmethod
    def bomb():
        t = TableDef([4, 22, 39, 48],
                     ['i','s','s','f'],
                     ['idBomb', 'uheMont', 'uheJus', 'vazBomb'],
                     [None, None, None, 'm3/s'])
        return t
    
    @staticmethod
    def cortesAtivos():
        t = TableDef([9, 29],
                     ['i','f'],
                     ['iteracao', 'multiplicador'],
                     [None, None])
        return t

    @staticmethod
    def custos():
        t = TableDef([25, 34],
                     ['s','f'],
                     ['descricao', 'valor'],
                     [None, None])
        return t

class pdo_operacao(pdo_base_oper):
    def __init__(self):
        super().__init__()
        self.addBlockType('interval')
    
    def getTableSet(self):
        return {'1': OperTableDef.balHidr(),
                 '2': OperTableDef.vazoes(),
                 '2B': OperTableDef.bomb(),
                 '3': OperTableDef.gerHidr(),
                 '4': TableDef.gerTerm(),
                 '5a': TableDef.intercambioEnergetico(),
                 '5b': TableDef.intercambioEletrico(),
                 '6': TableDef.gerItaipu(),
                 '7': TableDef.energiaContratada(),
                 '8a': TableDef.balancoEnergetico(),
                 '8b': TableDef.balancoEletrico(),
                 '9': OperTableDef.custos(),
                 '10': OperTableDef.cortesAtivos()}
    
    def checkOpenBlock_interval(self, line):
        dtrex = '(\d{2})\/(\d{2})\/(\d{4}) - (\d{2})\:(\d{2})'
        rex = 'PERIODO:\s*(\d*)  -  '+dtrex+' a '+dtrex
        m = re.match(rex, line)
        if not m:
            return False
        d = int(m.group(1))
        dts = datetime(int(m.group(4)),
                       int(m.group(3)),
                       int(m.group(2)),
                       int(m.group(5)),
                       int(m.group(6)))
        dte = datetime(int(m.group(9)),
                       int(m.group(8)),
                       int(m.group(7)),
                       int(m.group(10)),
                       int(m.group(11)))
        dtf = '%Y-%m-%dT%H:%M'
        bidx = [dts.strftime(dtf), dte.strftime(dtf)]
        self.setOpenBlock('interval', d)
        self.setBlockIndex(bidx)
        return True
    
    def readFile(self, fileName):
        modo = None
        with self.openFile(fileName) as f:
            for line in f:
                ln = line.strip()
                if self.checkOpenBlock_interval(ln):
                    modo = None
                if self.checkOpenTable(ln):
                    if self.openTableKey == '9':
                        modo = 'data'
                    else:
                        modo = 'header'
                elif modo == 'header':
                    if self.checkHeaderLimit(ln):
                        modo = 'data'
                    else:
                        self.readHeaderLine(line)
                elif modo == 'data':
                    if self.checkEndOfTable(ln):
                        modo = None
                    else:
                        self.readDataLine(line)
        
        f.close()
    