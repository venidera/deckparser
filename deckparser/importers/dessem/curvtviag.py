'''
Created on 22 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class curvtviag(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'curvtviag.xml'}
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isEOF(line):
                    break
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                tab = self.getTable('LN')
                if tab is not None:
                    self.getTable('LN').parseLine(line)
                else:
                    tab = self.getTable('CURVTV')
                    self.getTable('CURVTV').parseLine(line)
        f.close()
    