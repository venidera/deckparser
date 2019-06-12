from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class renovaveis(dsFile):
    
    def _dsFile__getConfig(self):
        return {'xml': 'renovaveis.xml'}
    
    def readLine(self, line):
        ln = line.strip()
        if ln.startswith('EOLICASUBM'):
            self.getTable('EOLICASUBM').parseLine(line)
        elif ln.startswith('EOLICA-GERACAO'):
            self.getTable('EOLICA-GERACAO').parseLine(line)
        elif ln.startswith('EOLICA'):
            self.getTable('EOLICA').parseLine(line)
    
    def readDSFile(self, fileName):
        with self.openDSFile(fileName) as f:
            for line in f:
                if record.isComment(line) or record.isBlankLine(line):
                    continue
                self.readLine(line)
        f.close()
