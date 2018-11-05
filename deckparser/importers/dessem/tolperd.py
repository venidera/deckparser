'''
Created on 22 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record


class tolperd(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isEOF(line):
                    break
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                
                nc = self.recGeral.parse(line)['nomeCampo']
                self.getTable(nc).parseLine(line)
        f.close()
    