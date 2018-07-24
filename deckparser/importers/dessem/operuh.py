'''
Created on 4 de jul de 2018

@author: Renan
'''
from core.dsFile import dsFile
from core.record import record


class operuh(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readLine(self, line):
        r = self.getRec('Restr').parse(line)
        if r['nomeCampo'] != 'OPERUH':
            raise ValueError('Campo invalido')
        
        if r['nomeRestr'] == 'REST':
            self.getTable('REST').parseLine(line)
        elif r['nomeRestr'] == 'ELEM':
            self.getTable('ELEM').parseLine(line)
        elif r['nomeRestr'] == 'LIM':
            self.getTable('LIM').parseLine(line)
        elif r['nomeRestr'] == 'VAR':
            self.getTable('VAR').parseLine(line)
    
    def readDSFile(self, fileName):
        nRec = 0
        with open(fileName, 'r') as f:
            for line in f:
                nRec = nRec + 1
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                self.readLine(line)
        f.close()
