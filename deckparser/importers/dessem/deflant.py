'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class deflant(dsFile):
    def __init__(self):
        dsFile.__init__(self)
    
    def _dsFile__getConfig(self):
        return {'xml': 'deflant.xml'}
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                
                self.getTable('DEFANT').parseLine(line)
        f.close()
    