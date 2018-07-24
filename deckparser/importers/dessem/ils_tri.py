'''
Created on 22 de jul de 2018

@author: Renan
'''
from core.dsFile import dsFile
from core.record import record


class ils_tri(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readDSFile(self, fileName):
        nRec = 0
        with open(fileName, 'r') as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isEOF(line):
                    break
                if nRec == 2:
                    self.getRec('Nivel').parse(line)
                elif nRec >= 3:
                    self.getTable('Vazoes').parseLine(line)
        f.close()
    