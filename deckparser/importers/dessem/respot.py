'''
Created on 4 de jul de 2018

@author: Renan
'''
from core.dsFile import dsFile
from core.record import record


class respot(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
        # TODO Bloco USI
    
    def isEOF(self, line):
        return record.assertString(line, '9999')
    
    def readDSFile(self, fileName):
        nRec = 0
        with open(fileName, 'r') as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                if self.isEOF(line):
                    break
                
                r = self.getRec('Geral').parse(line)
                if r['nomeCampo'] == 'RP':
                    self.getTable('RP').parseLine(line)
                elif r['nomeCampo'] == 'LM':
                    self.getTable('LM').parseLine(line)
        f.close()
    