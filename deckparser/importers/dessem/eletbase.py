'''
Created on 5 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dsFile import dsFile
from deckparser.importers.dessem.core.record import record

class eletbase(dsFile):
    def __init__(self, muda=False):
        self.muda = muda
        dsFile.__init__(self)
        
    def _dsFile__getConfig(self):
        if self.muda:
            return {'xml': 'eletmodif.xml'}
        return {'xml': 'eletbase.xml'}
    
    def newVersionDBAR(self):
        t = self.getTable('DBAR')
        t.setRange('idBarra', [1, 4])
        t.setRange('nivelTensao', [9, 9])
        t.setRange('nomeBarra', [10, 21])
        t.setRange('angTensao', [27, 30])
        t.setRange('potAtiva', [31, 35])
        t.setRange('cargaAtiva', [56, 60])
        t.setRange('idArea', [71, 72])
        t.setRange('idSistema', [77, 78])
    
    def newVersionDLIN(self):
        t = self.getTable('DLIN')
        t.setRange('idBarraOrig', [1, 5])
        t.setRange('codOper', [8, 8])
        t.setRange('idBarraDest', [11, 15])
        t.setRange('idCircuito', [16, 17])
        t.setRange('flagDelisga', [18, 18])
        t.setRange('refArea', [19, 19])
        t.setRange('resistencia', [21, 26])
        t.setRange('reatancia', [27, 32])
        t.setRange('tapNominal', [39, 43])
        t.setRange('angDefasagem', [54, 58])
        t.setRange('capFluxoNorm', [65, 68])
        t.setRange('capFluxoEmerg', [69, 72])
        t.setRange('flagViolacao', [97, 97])
        t.setRange('flagPerdas', [99, 99])
        
    def newVersionDCSC(self):
        t = self.getTable('DCSC')
        t.setRange('idBarraOrig', [1, 5])
        t.setRange('codOper', [8, 8])
        t.setRange('idBarraDest', [11, 15])
        t.setRange('idCircuito', [16, 17])
        t.setRange('reatancia', [38, 43])
        
    def newVersionDARE(self):
        t = self.getTable('DARE')
        t.setRange('idArea', [1, 3])
        t.setRange('nomeArea', [19, 54])
        
    def newVersionDANC(self):
        t = self.getTable('DANC')
        t.setRange('idArea', [1, 3])
        t.setRange('fatorCarga', [5, 10])
        
    def newVersionDGBT(self):
        t = self.getTable('DGBT')
        t.setRange('nivelTensao', [1, 2])
        t.setRange('tensaoNominal', [4, 8])
        
    def newVersionDUSI(self):
        self.getTable('DUSI').setRange('idBarra', [7, 11])
    
    def newVersionDREF(self):
        self.getTable('DREF_comp').setRange('idBarra', [6, 10])
        self.getTable('DREF_comp').setRange('idBarraDest', [11, 15])
    
    def isComment(self, line):
        return line[0] == '('
    
    def isFimBloco(self, line):
        return record.assertString(line, '9999') or record.assertString(line, '99999')
    
    def detectMode(self, line, sufix):
        for name in self.records:
            if record.assertString(line, name + sufix):
                return name
        for name in self.tables:
            if record.assertString(line, name + sufix):
                return name
        return None
        
    def readLine(self, line, mode):
        if mode == 'DREF':
            if line.startswith('RESP'):
                self.getTable('DREF').parseLine(line)
            else:
                self.getTable('DREF_comp').parseLine(line)
                self.getTable('DREF_comp').setField('idRestr', self.getTable('DREF').getField('idRestr'))
        elif mode in self.records:
            self.getRec(mode).parse(line)
        elif mode in self.tables:
            self.getTable(mode).parseLine(line)
    
    def readDSFile(self, fileName):
        nRec = 0
        modo = None
        sufix = ' MUDA' if self.muda else ''
        
        # Aparentemente esta trocada a especificacao da versao antiga com a nova no manual
        #self.newVersionDBAR()
        self.newVersionDLIN()
        self.newVersionDCSC()
        self.newVersionDARE()
        self.newVersionDANC()
        self.newVersionDGBT()
        self.newVersionDUSI()
        self.newVersionDREF()
        
        with self.openDSFile(fileName) as f:
            for line in f:
                nRec = nRec + 1
                
                if self.isComment(line) or record.isBlankLine(line):
                    continue
                if self.isFimBloco(line):
                    modo = None
                    continue
                
                m = self.detectMode(line, sufix)
                if m is not None:
                    modo = m
                else:
                    try:
                        self.readLine(line, modo)
                    except ValueError:
                        print('Record: {:s}'.format(modo))
                        raise
        f.close()
        