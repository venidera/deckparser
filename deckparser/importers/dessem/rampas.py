from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class rampas(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'rampas.xml'}
    
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
                    break
                if modo:
                    self.getTable('RAMP').parseLine(line)
                if record.assertString(line, 'RAMP'):
                    modo = True
        f.close()
