'''
Created on 5 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record
import deckparser.importers.dessem.v2.cfg as cfg_v2

class termdat(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'termdat.xml'}
    
    def getConfigPath(self):
        return cfg_v2.__path__[0]
    
    def readLine(self, line):
        r = self.getRec('Campo').parse(line)
        
        if r['nomeCampo'] == 'CADUSIT':
            self.getTable('CADUSIT').parseLine(line)
        elif r['nomeCampo'] == 'CADUNIDT':
            self.getTable('CADUNIDT').parseLine(line)
        elif r['nomeCampo'] == 'CADCONF':
            self.getTable('CADCONF').parseLine(line)
        elif r['nomeCampo'] == 'CADMIN':
            self.getTable('CADMIN').parseLine(line)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                self.readLine(line)
        f.close()
