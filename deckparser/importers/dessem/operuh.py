'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class operuh(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'operuh.xml'}
    
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
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                self.readLine(line)
        f.close()
