from deckparser.importers.dessem.out.pdo_sist import pdo_sist
from deckparser.importers.dessem.out.pdo_operacao import pdo_operacao
from deckparser.importers.dessem.out.pdo_sumaoper import pdo_sumaoper
import logging
import os

class ResultLoader:
    def __init__(self, dirDS=None, fileEncoding=None):
        self.dirDS = dirDS
        self.fileEncoding = fileEncoding
        self.file_filter = None
        self.init()
    
    ''' Inicializa as instancias dos importers '''
    def init(self):
        self.getLogger().info('Loading configuration')
        m = {}
        m['pdo_sist'] = pdo_sist()
        m['pdo_operacao'] = pdo_operacao()
        m['pdo_sumaoper'] = pdo_sumaoper()
        self.resultLoaders = m
    
    def listFiles(self):
        return list(self.resultLoaders.keys())
    
    def setDirDS(self, dirDS):
        self.dirDS = dirDS
    
    def getFileList(self):
        return [f for f in self.resultLoaders.keys() if self.filterFile(f)]
    
    def get(self, fileType):
        return self.resultLoaders.get(fileType)
        
    def setFileFilter(self, file_filter):
        self.file_filter = file_filter
        
    def filterFile(self, f):
        ff = self.file_filter
        if ff is None:
            return True
        if f in ff:
            return True
        return False
    
    def loadAll(self):
        for f in self.resultLoaders:
            if self.filterFile(f):
                self.load(f)
    
    def __get_matching_filename(self, fk):
        for f in os.listdir(self.dirDS):
            if f.lower() == fk.lower() + '.dat':
                return f
    
    def load(self, fk):
        fn = self.__get_matching_filename(fk)
        if not fn:
            self.getLogger().warn('Missing file: %s', str(fk))
        fp = os.path.join(self.dirDS, fn)
        try:
            self.resultLoaders[fk].readFile(fp)
        except FileNotFoundError:
            self.getLogger().warn('Missing file: %s', str(fp))
    
    def getData(self, fmt=None):
        dd = {}
        for f in self.resultLoaders:
            if not self.filterFile(f):
                continue
            ds = self.resultLoaders[f]
            if fmt == 'dict':
                dd[f] = ds.export()
            else:
                dd[f] = ds
        return dd
    
    def getLogger(self):
        return logging.getLogger(__name__)
    