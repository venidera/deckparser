'''
Created on 5 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class termdat(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'termdat.xml'}
    
    def readLine(self, line):
        r = self.getRec('Campo').parse(line)
        
        if r['nomeCampo'] == 'CADUSIT':
            self.getTable('CADUSIT').parseLine(line)
        elif r['nomeCampo'] == 'CADUNIDT':
            self.getTable('CADUNIDT').parseLine(line)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                self.readLine(line)
        f.close()
