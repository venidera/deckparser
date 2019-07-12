import re
from datetime import datetime, timedelta
from deckparser.importers.dessem.out.pdo_base_oper import pdo_base_oper

def init_datetime(y, m, d, h, mn):
    delta_d = 0
    if h == 24:
        h = 0
        delta_d = 1
    return datetime(y,m,d,h,mn) + timedelta(days=delta_d)

class pdo_operacao(pdo_base_oper):
    def __init__(self):
        super().__init__('pdo_operacao')
        self.addBlockType('interval')

    def checkOpenBlock_interval(self, line):
        dtrex = '(\d{2})\/(\d{2})\/(\d{4}) - (\d{2})\:(\d{2})'
        rex = 'PERIODO:\s*(\d*)  -  '+dtrex+' a '+dtrex
        m = re.match(rex, line)
        if not m:
            return False
        d = int(m.group(1))
        dts = init_datetime(int(m.group(4)),
                           int(m.group(3)),
                           int(m.group(2)),
                           int(m.group(5)),
                           int(m.group(6)))
        dte = init_datetime(int(m.group(9)),
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
    