from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class rstlpp(dsFile):
    def __init__(self):
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        return {'xml': 'rstlpp.xml'}
    
    def detectTable(self, line):
        nc = line.split()[0]
        return self.getTable(nc)
    
    def readLine(self, line):
        t = self.detectTable(line)
        if t:
            t.parseLine(line)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                self.readLine(line)
        f.close()
