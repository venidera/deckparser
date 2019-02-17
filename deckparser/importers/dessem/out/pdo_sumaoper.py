import re
from datetime import date
from deckparser.importers.dessem.out.pdo_base_oper import pdo_base_oper

class pdo_sumaoper(pdo_base_oper):
    def __init__(self):
        super().__init__('pdo_sumaoper')
        self.addBlockType('day')
        self.addBlockType('week')
    
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
    