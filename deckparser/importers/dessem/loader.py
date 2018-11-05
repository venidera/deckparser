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
from deckparser.importers.dessem.simul import simul
from datetime import datetime
import os

''' Classe responsavel por carregar os arquivos do DESSEM usando o pacote importers.'''
class Loader:
    def __init__(self, dirDS):
        self.dirDS = dirDS
        self.init()
        self.loadIndex()
    
    ''' Inicializa as instancias dos importers e os indices de arquivos '''
    def init(self):
        print('Carregando arquivos de configuracao')
        m = {}
        m['hidr'] = HIDR()
        m['dessem'] = dessem(self.xmlKey('dessem'))
        m['desselet'] = desselet(self.xmlKey('desselet'))
        m['entdados'] = entdados(self.xmlKey('entdados'))
        m['operuh'] = operuh(self.xmlKey('operuh'))
        m['dadvaz'] = dadvaz(self.xmlKey('dadvaz'))
        m['deflant'] = deflant(self.xmlKey('deflant'))
        m['termdat'] = termdat(self.xmlKey('termdat'))
        m['operut'] = operut(self.xmlKey('operut'))
        m['ptoper'] = ptoper(self.xmlKey('ptoper'))
        m['areacont'] = areacont(self.xmlKey('areacont'))
        m['respot'] = respot(self.xmlKey('respot'))
        m['simul'] = simul(self.xmlKey('simul'))
        m['curvtviag'] = simul(self.xmlKey('curvtviag'))
        m['ils_tri'] = simul(self.xmlKey('ils_tri'))
        m['cotasr11'] = simul(self.xmlKey('cotasr11'))
        self.dsFileMap = m
        self.index = {}
        self.indexMap = {'entdados': 'dadger', 'dadvaz': 'vazoes', 'hidr': 'cadusih', 
                         'termdat': 'cadterm', 'desselet': 'indelet'}
        
        self.eletIndex = {'base': {}, 'modif': {}}
        self.eletData = {'base': {}, 'modif': {}}
        self.initEletBase()
        self.initEletModif()
        
    def initEletBase(self):
        d = eletbase(self.xmlKey('eletbase'))
        self.dsFileMap['eletbase'] = d
        return d
    
    def initEletModif(self):
        d = eletbase(self.xmlKey('eletmodif'), muda=True)
        self.dsFileMap['eletmodif'] = d
        return d
    
    ''' Chave do tipo xml para cargarregar os importers '''
    def xmlKey(self, cfgFile):
        return {'xml': cfgFile + '.xml'}
    
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
        if nome not in self.index:
            return None
        return self.index[nome].get('arquivo')
    
    ''' Carga de arquivos tipo texto '''
    def load(self, dsFileName, fileType):
        if fileType == 'hidr':
            self.loadHIDR(dsFileName)
            return
        if dsFileName is None:
            dsFileName = self.getArq(fileType)
        if dsFileName is None:
            print('Arquivo do tipo "{:s}" ausente no indice'.format(fileType))
            return
        else:
            print('Carregando arquivo "{:s}" do tipo "{:s}"'.format(dsFileName, fileType))
        dsf = self.dsFileMap[fileType]
        dsf.clearData()
        fullPath = os.path.join(self.dirDS, dsFileName)
        dsf.readDSFile(fullPath)
        
    def loadAll(self):
        for f in self.dsFileMap:
            if f in ['dessem','eletbase','eletmodif']:
                continue
            self.load(None, f)
        self.loadElet()
    
    def loadDessem(self, dsFileName):
        self.load(dsFileName, 'dessem')
        for r in self.get('dessem').getTable('Arq').getData():
            self.addIndex(r['arquivo'], r['descricao'], r['nomeArquivo'])

    def loadDesselet(self, dsFileName=None):
        self.load(dsFileName, 'desselet')
        
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
    
    def getEletIntervalCodList(self):
        return self.eletIndex['modif'].keys()
    
    def loadElet(self, intCodList=None):
        if intCodList is None:
            intCodList = self.getEletIntervalCodList()
            
        intCodBaseList = []
        for i in intCodList:
            r = self.eletIndex['modif'][i]
            p = r['patamar']
            if p not in intCodBaseList:
                intCodBaseList.append(p)
        
        for i in intCodBaseList:
            dsb = self.initEletBase()
            r = self.eletIndex['base'][i]
            self.loadEletBase(r['arquivo'])
            self.eletData['base'][i] = dsb
            
        for i in intCodList:
            dsm = self.initEletModif()
            r = self.eletIndex['modif'][i]
            self.loadEletModif(r['arquivo'])
            self.eletData['modif'][i] = dsm

    def searchHIDR(self, dsFileName, nome):
        h = HIDR()
        h.search(self.dirDS + dsFileName, nome)
        return h
    
    def loadHIDR(self, dsFileName=None):
        if dsFileName is None:
            dsFileName = self.getArq('hidr')
        print('Carregando arquivo "{:s}" do tipo "{:s}"'.format(dsFileName, 'hidr'))
        h = self.dsFileMap['hidr']
        h.clearData()
        fullPath = os.path.join(self.dirDS, dsFileName)
        h.readFile(fullPath)
    
    def loadEntdados(self, dsFileName=None):
        self.load(dsFileName, 'entdados')

    def loadOperUH(self, dsFileName=None):
        self.load(dsFileName, 'operuh')

    def loadDadvaz(self, dsFileName=None):
        self.load(dsFileName, 'dadvaz')
    
    def loadDeflant(self, dsFileName=None):
        self.load(dsFileName, 'deflant')

    def loadEletBase(self, dsFileName=None):
        self.load(dsFileName, 'eletbase')

    def loadEletModif(self, dsFileName=None):
        self.load(dsFileName, 'eletmodif')

    def loadTerm(self, dsFileName=None):
        self.load(dsFileName, 'termdat')

    def loadOperut(self, dsFileName=None):
        self.load(dsFileName, 'operut')

    def loadPtoper(self, dsFileName=None):
        self.load(dsFileName, 'ptoper')

    def loadAreacont(self, dsFileName=None):
        self.load(dsFileName, 'areacont')

    def loadRespot(self, dsFileName=None):
        self.load(dsFileName, 'respot')
    
    def toDict(self):
        dd = {}
        for f in self.dsFileMap:
            if f in ['eletbase', 'eletmodif']:
                continue
            ds = self.dsFileMap[f]
            if not ds.isEmpty():
                dd[f] = ds.toDict()
        dd['elet'] = self.eletToDict()
        return dd
    
    def eletToDict(self):
        dd = {'base': {}, 'modif': {}}
        edb = self.eletData['base']
        for i in edb:
            dd['base'][i] = edb[i].toDict()
        edm = self.eletData['modif']
        for i in edm:
            dd['modif'][i] = edm[i].toDict()
        return dd
    