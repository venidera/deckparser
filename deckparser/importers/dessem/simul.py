'''
Created on 25 de out de 2018

@author: Renan Maciel
'''

from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class simul(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'simul.xml'}
        
    def endOfBlock(self, line):
        return record.assertString(line, 'FIM')
    
    def readDSFile(self, fileName):
        nRec = 0
        modo = None
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isEOF(line):
                    break
                if self.endOfBlock(line):
                    modo = None
                    continue
                if nRec == 3:
                    self.getRec('Cabecalho').parse(line)
                
                nc = line[0:5]
                if nc == 'DISC': modo = 'DISC'
                elif nc == 'VOLI': modo = 'VOLI'
                elif nc == 'OPER': modo = 'OPER'
                
                if modo is not None:
                    self.getTable(modo).parseLine(line)
        f.close()
