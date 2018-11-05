'''
Created on 6 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record


class entdados(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readLine(self, line):
        ls = line.strip()
        
        for size in range(6, 2, -1):
            name = ls[0:size-1]
            
            if name == 'META':
                meta = self.getRec('META').parse(line)
                if meta['nomeCampo2'] == 'CJSIST':
                    self.getTable('META_CJSIST').parseLine(line)
                elif meta['nomeCampo2'] == 'RECEB':
                    self.getTable('META_RECEB').parseLine(line)
                elif meta['nomeCampo2'] == 'GTER':
                    self.getTable('META_GTER').parseLine(line)
                break
            elif name in self.records:
                self.getRec(name).parse(line)
                break
            elif name in self.tables:
                self.getTable(name).parseLine(line)
                break
            elif name in ['CI', 'CE']:
                self.getTable('CICE').parseLine(line)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isComment(line) or record.isBlankLine(line):
                    continue

                self.readLine(line)
        f.close()
