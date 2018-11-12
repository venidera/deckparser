'''
Created on 5 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class dessem(dsFile):
    def __init__(self):
        dsFile.__init__(self)
    
    def _dsFile__getConfig(self):
        return {'xml': 'dessem.xml'}
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line):
                    continue
                self.getTable('Arq').parseLine(line)
        f.close()
