'''
Created on 22 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class ils_tri(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'ils_tri.xml'}
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isEOF(line):
                    break
                if nRec == 2:
                    self.getRec('Nivel').parse(line)
                elif nRec >= 3:
                    if len(line) > 3 and line[:3] == 'MAX':
                        self.getRec('VazoesMax').parse(line)
                    else:
                        self.getTable('Vazoes').parseLine(line)
        f.close()
    