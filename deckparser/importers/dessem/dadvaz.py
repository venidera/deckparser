'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record


class dadvaz(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isEOF(line):
                    break
                if nRec == 10:
                    self.getRec('DataHora').parse(line)
                if nRec == 13:
                    self.getRec('Cabecalho').parse(line)
                if nRec >= 17:
                    self.getTable('Vazoes').parseLine(line)
        f.close()
