from deckparser.importers.dessem.out.pdo_sist import pdo_sist
from deckparser.importers.dessem.out.pdo_operacao import pdo_operacao
from deckparser.importers.dessem.out.pdo_sumaoper import pdo_sumaoper
import logging
import os
import re

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
    
    def prepare(self):
        dessem_version = self.loadDessemVersion()
        self.getLogger().info('Preparing configuration (DESSEM version {:s})'.format(str(dessem_version)))
        for fk in ['pdo_sumaoper','pdo_operacao']:
            self.resultLoaders[fk].applyModif(dessem_version)
    
    def openFile(self, fn):
        fp = os.path.join(self.dirDS, fn)
        return open(fp, 'r', encoding='iso-8859-1')
    
    def loadDessemVersion(self):
        for fk in ['pdo_sist','pdo_operacao']:
            fn = self.__get_matching_filename(fk)
            if not fn:
                continue
            with self.openFile(fn) as fp:
                for ln in fp:
                    v = self.__readDessemVersion(ln)
                    if v:
                        return v
    
    def __readDessemVersion(self, ln):
        rex = ".*VERSAO\s*([0-9]{2})(\.[0-9]{2}){0,1}.*"
        m = re.match(rex, ln)
        if m:
            v =  [int(v_.strip('.')) if v_ else 0 for v_ in m.groups()]
            return tuple(v)
    
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
        self.prepare()
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
            return
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
    