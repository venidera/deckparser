'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record


class operut(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
        self.ucterm = False
        self.flgucterm = False
    
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
                
                if record.assertString(line, 'UCTERM'):
                    self.ucterm = True
                elif record.assertString(line, 'FLGUCTERM'):
                    self.flgucterm = True
                elif record.assertString(line, 'INIT'):
                    modo = 'INIT'
                elif record.assertString(line, 'OPER'):
                    modo = 'OPER'
                elif modo == 'INIT':
                    self.getTable('INIT').parseLine(line)
                elif modo == 'OPER':
                    self.getTable('OPER').parseLine(line)
        f.close()
    