'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class areacont(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'areacont.xml'}
    
    def readDSFile(self, fileName):
        nRec = 0
        modo = None
        with self.openDSFile(fileName) as f:
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
    