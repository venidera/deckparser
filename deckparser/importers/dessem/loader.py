'''
Created on 10 de out de 2018

@author: Renan Maciel
'''
from deckparser.importers.dessem.hidr import HIDR
from deckparser.importers.dessem.dessem import dessem
from deckparser.importers.dessem.desselet import desselet
from deckparser.importers.dessem.entdados import entdados
from deckparser.importers.dessem.operuh import operuh
from deckparser.importers.dessem.dadvaz import dadvaz
from deckparser.importers.dessem.eletbase import eletbase
from deckparser.importers.dessem.termdat import termdat
from deckparser.importers.dessem.ptoper import ptoper
from deckparser.importers.dessem.operut import operut
from deckparser.importers.dessem.deflant import deflant
from deckparser.importers.dessem.areacont import areacont
from deckparser.importers.dessem.respot import respot
from deckparser.importers.dessem.curvtviag import curvtviag
from deckparser.importers.dessem.ils_tri import ils_tri
from deckparser.importers.dessem.cotasr11 import cotasr11
from deckparser.importers.dessem.simul import simul
from datetime import datetime
import os
import logging

''' Classe responsavel por carregar os arquivos do DESSEM usando o pacote importers.'''
class Loader:
    def __init__(self, dirDS, fileEncoding=None):
        self.dirDS = dirDS
        self.fileEncoding = fileEncoding
        self.init()
        self.loadIndex()
    
    ''' Inicializa as instancias dos importers e os indices de arquivos '''
    def init(self):
        self.getLogger().info('Loading configuration files')
        m = {}
        m['hidr'] = HIDR()
        m['dessem'] = dessem()
        m['desselet'] = desselet()
        m['entdados'] = entdados()
        m['operuh'] = operuh()
        m['dadvaz'] = dadvaz()
        m['deflant'] = deflant()
        m['termdat'] = termdat()
        m['operut'] = operut()
        m['ptoper'] = ptoper()
        m['areacont'] = areacont()
        m['respot'] = respot()
        m['simul'] = simul()
        m['curvtviag'] = curvtviag()
        m['ils_tri'] = ils_tri()
        m['cotasr11'] = cotasr11()
        
        if self.fileEncoding:
            for k in m:
                if k != 'hidr':
                    m[k].setEncoding(self.fileEncoding)
        
        self.dsFileMap = m
        self.index = {}
        self.indexMap = {'entdados': 'dadger', 'dadvaz': 'vazoes', 'hidr': 'cadusih', 
                         'termdat': 'cadterm', 'desselet': 'indelet'}
        
        self.eletIndex = {'base': {}, 'modif': {}}
        self.eletData = {'base': {}, 'modif': {}}
        self.initEletBase()
        self.initEletModif()
        
    def initEletBase(self):
        d = eletbase()
        self.dsFileMap['eletbase'] = d
        return d
    
    def initEletModif(self):
        d = eletbase(muda=True)
        self.dsFileMap['eletmodif'] = d
        return d

    ''' Get para importer '''
    def get(self, fileType):
        return self.dsFileMap.get(fileType)
    
    ''' Carrega o indice de arquivos do DESSEM '''
    def loadIndex(self):
        self.loadDessem('dessem.arq')
        self.loadEletIndex()
    
    ''' Carrega o indice de arquivos dos dados eletricos '''
    def loadEletIndex(self):
        self.loadDesselet()
    
    ''' Adiciona um indice de arquivo '''
    def addIndex(self, nome, descricao, nomeArq):
        self.index[nome.lower()] = {'arquivo': nomeArq, 'descricao': descricao}
    
    ''' Adiciona um indice de arquivo de base de dados da rede eletrica'''
    def addEletBaseIndex(self, cod, nome, nomeArq):
        self.eletIndex['base'][cod] = {'nome': nome, 'arquivo': nomeArq.replace(' ', '')} # nome do arquivo e extensao estao separados por espacos
    
    ''' Adiciona um indice de arquivo de modificacao de dados da rede eletrica'''
    def addEletModifIndex(self, cod, nome, nomeArq, codCaso, period):
        self.eletIndex['modif'][cod] = {'nome': nome, 'arquivo': nomeArq, 'patamar': codCaso, 'period': period}
    
    '''Get para o nome de arquivo carregado pelo indice '''
    def getArq(self, nome):
        if nome in self.index:
            return self.index[nome].get('arquivo')
        if nome in self.indexMap:
            nome = self.indexMap[nome]
        if nome in self.index:
            return self.index[nome].get('arquivo')
        return None
    
    def getLogger(self):
        return logging.getLogger(__name__)
    
    ''' Carga de arquivos tipo texto '''
    def load(self, fileType, dsFileName):
        if dsFileName is None:
            dsFileName = self.getArq(fileType)
        if dsFileName is None:
            self.getLogger().warning('Missing index for file type: %s', str(fileType))
            return
        else:
            self.getLogger().info('Loading file: %s (%s)', dsFileName, fileType)
        dsf = self.dsFileMap[fileType]
        dsf.clearData()
        fullPath = os.path.join(self.dirDS, dsFileName)
        dsf.readDSFile(fullPath)
    
    def loadAll(self):
        for f in self.dsFileMap:
            if f not in ['dessem','eletbase','eletmodif']:
                self.load(f, None)
        self.loadElet()
    
    def loadDessem(self, dsFileName):
        self.load('dessem', dsFileName)
        for r in self.get('dessem').getTable('Arq').getData():
            self.addIndex(r['arquivo'], r['descricao'], r['nomeArquivo'])

    def loadDesselet(self, dsFileName=None):
        self.load('desselet', dsFileName)
        
        for r in self.get('desselet').getTable('Base').getData():
            self.addEletBaseIndex(r['idCaso'], r['nomeCaso'], r['nomeArquivo'])
        
        for r in self.get('desselet').getTable('Modif').getData():
            ini = datetime(r['ano'], r['mes'], r['dia'], r['hora'], r['minuto'])
            period = {'inicio': ini, 'duracao': r['duracao']}
            self.addEletModifIndex(r['periodo'], r['nomePeriodo'], r['nomeArquivo'], r['idCaso'], period)
    
    def getEletBase(self, i):
        p = self.eletIndex['modif'][i]['patamar']
        return self.eletData['base'][p]
    
    def getEletModif(self, i):
        return self.eletData['modif'][i]
    
    def getEletCodList(self):
        return self.eletIndex['modif'].keys()
    
    def getEletCodBaseSet(self, intCodList):
        s = set()
        for i in intCodList:
            r = self.eletIndex['modif'].get(i)
            if r is None:
                self.getLogger().warning('No elet base index for interval: %d', i)
            else:
                s.add(r['patamar'])
        return s

    def loadElet(self, intCodList=None):
        if intCodList is None:
            intCodList = self.getEletCodList()
        intCodBaseList = self.getEletCodBaseSet(intCodList)
        
        for i in intCodBaseList:
            self.__loadEletBase(i)
        for i in intCodList:
            self.__loadEletModif(i)
    
    def __loadEletBase(self, i):
        r = self.eletIndex['base'].get(i)
        if r is None:
            self.getLogger().warning('eletbase: Undefined base interval: %d', i)
            return
        dsb = self.initEletBase()
        self.loadEletBase(r['arquivo'])
        self.eletData['base'][i] = dsb
    
    def __loadEletModif(self, i):
        r = self.eletIndex['modif'].get(i)
        if r is None:
            self.getLogger().warning('eletmodif: Undefined interval: %d', i)
            return
        dsm = self.initEletModif()
        self.loadEletModif(r['arquivo'])
        self.eletData['modif'][i] = dsm
    
    def loadHIDR(self, dsFileName=None):
        self.load('hidr', dsFileName)

    def loadEntdados(self, dsFileName=None):
        self.load('entdados', dsFileName)

    def loadOperUH(self, dsFileName=None):
        self.load('operuh', dsFileName)

    def loadDadvaz(self, dsFileName=None):
        self.load('dadvaz', dsFileName)
    
    def loadDeflant(self, dsFileName=None):
        self.load('deflant', dsFileName)

    def loadEletBase(self, dsFileName=None):
        self.load('eletbase', dsFileName)

    def loadEletModif(self, dsFileName=None):
        self.load('eletmodif', dsFileName)

    def loadTerm(self, dsFileName=None):
        self.load('termdat', dsFileName)

    def loadOperut(self, dsFileName=None):
        self.load('operut', dsFileName)

    def loadPtoper(self, dsFileName=None):
        self.load('ptoper', dsFileName)

    def loadAreacont(self, dsFileName=None):
        self.load('areacont', dsFileName)

    def loadRespot(self, dsFileName=None):
        self.load('respot', dsFileName)
    
    def loadCurvtviag(self, dsFileName=None):
        self.load('curvtviag', dsFileName)
    
    def loadIlstri(self, dsFileName=None):
        self.load('ils_tri', dsFileName)
    
    def loadCotasR11(self, dsFileName=None):
        self.load('cotasr11', dsFileName)
    
    def loadSimul(self, dsFileName=None):
        self.load('simul', dsFileName)
    
    def getData(self, fmt=None):
        dd = {}
        for f in self.dsFileMap:
            if f in ['eletbase', 'eletmodif']:
                continue
            ds = self.dsFileMap[f]
            if fmt == 'dict':
                dd[f] = ds.toDict()
            else:
                dd[f] = ds
        dd['elet'] = self.getEletData(fmt)
        return dd
    
    def getEletData(self, fmt):
        dd = {'base': {}, 'modif': {}}
        edb = self.eletData['base']
        for i in edb:
            if fmt == 'dict':
                dd['base'][i] = edb[i].toDict()
            else:
                dd['base'][i] = edb[i]
        edm = self.eletData['modif']
        for i in edm:
            if fmt == 'dict':
                dd['modif'][i] = edm[i].toDict()
            else:
                dd['modif'][i] = edm[i]
        return dd
    