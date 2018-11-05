'''
Created on 12 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record


class infofcf(dsFile):
    def __init__(self, cfg=None):
        dsFile.__init__(self, cfg)
    
    def readDSFile(self, fileName):
        nRec = 0
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if record.isBlankLine(line) or record.isComment(line):
                    continue
                if record.isEOF(line) or record.isComment(line):
                    break
                
                r = self.getRec('Geral').parse(line)
                if r['nomeCampo'] == 'MAPFCF':
                    m = self.getRec('MAPFCF').parse(line)
                    if m['nomeDado'] == 'SISGNL':
                        self.getTable('SISGNL').parseLine(line)
                    elif m['nomeDado'] == 'DURPAT':
                        self.getTable('DURPAT').parseLine(line)
                    elif m['nomeDado'] == 'TVIAG':
                        self.getTable('TVIAG').parseLine(line)
                    elif m['nomeDado'] == 'CGTMIN':
                        self.getTable('CGTMIN').parseLine(line)
                elif r['nomeCampo'] == 'FCFFIX':
                    self.getTable('FCFFIX').parseLine(line)
                
        f.close()
