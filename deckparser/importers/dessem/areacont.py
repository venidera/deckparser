'''
Created on 4 de jul de 2018

@author: Renan
'''
from core.dsFile import dsFile
from core.record import record


class areacont(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readDSFile(self, fileName):
        nRec = 0
        modo = None
        with open(fileName, 'r') as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                if record.assertString(line, 'FIM'):
                    continue
                if record.assertString(line, '9999'):
                    break
                
                if record.assertString(line, 'AREA'):
                    modo = 'AREA'
                elif record.assertString(line, 'USINA'):
                    modo = 'USINA'
                elif modo == 'AREA':
                    self.getTable('AREA').parseLine(line)
                elif modo == 'USINA':
                    self.getTable('USINA').parseLine(line)
        f.close()
    