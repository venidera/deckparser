'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record


class respot(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
        # TODO Bloco USI
    
    def isEOF(self, line):
        return record.assertString(line, '9999')
    
    def isEndOfBlock(self, line):
        return record.assertString(line, 'FIM')
    
    def readDSFile(self, fileName):
        nRec = 0
        modo = None
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                if self.isEndOfBlock(line):
                    modo = None
                    continue
                if self.isEOF(line):
                    break
                
                if modo == 'USI':
                    self.getTable('USI').parseLine(line)
                else:
                    ls = line.strip()
                    nc = ls[0:2]
                    if nc == 'RP':
                        self.getTable('RP').parseLine(line)
                    elif nc == 'LM':
                        self.getTable('LM').parseLine(line)
                    elif ls[0:3] == 'USI':
                        self.modo = 'USI'
                    
        f.close()
    