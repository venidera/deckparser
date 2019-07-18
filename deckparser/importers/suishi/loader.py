'''
Created on 17 de julho de 2019

@author: Makoto Kadowaki
'''
from deckparser.suishidicted import SuishiDicted
from unidecode import unidecode

# from deckparser.importers.dessem.hidr import HIDR
# from deckparser.importers.dessem.dessem import dessem
# from deckparser.importers.dessem.desselet import desselet
# from deckparser.importers.dessem.entdados import entdados
# from deckparser.importers.dessem.operuh import operuh
# from deckparser.importers.dessem.dadvaz import dadvaz
# from deckparser.importers.dessem.eletbase import eletbase
# from deckparser.importers.dessem.termdat import termdat
# from deckparser.importers.dessem.ptoper import ptoper
# from deckparser.importers.dessem.operut import operut
# from deckparser.importers.dessem.deflant import deflant
# from deckparser.importers.dessem.areacont import areacont
# from deckparser.importers.dessem.respot import respot
# from deckparser.importers.dessem.curvtviag import curvtviag
# from deckparser.importers.dessem.ils_tri import ils_tri
# from deckparser.importers.dessem.cotasr11 import cotasr11
# from deckparser.importers.dessem.simul import simul
# from deckparser.importers.dessem.renovaveis import renovaveis
# from deckparser.importers.dessem.v2.termdat import termdat as termdat_v2
# from datetime import datetime
# import os
import logging
''' Classe responsavel por carregar os arquivos do SUISHI usando o pacote importers.'''


class Loader:
    def __init__(self, dz=None):
        self.dd = SuishiDicted()
        self.dz = dz
        # self.dd.dirname = dz.dirname
        # self.dd.filename = dz.filename
        # self.dd.fhash = dz.fhash
        self.initialized = False
        if dz:
            self.initialized = self.init()

    ''' Inicializa as instancias dos importers e os indices de arquivos '''
    def init(self):
        self.getLogger().debug('Loading configuration files')
        self.load_InputData()
        return True

    def load_InputData(self):
        try:
            fobj = self.dz.z.open(self.dd.CaseStudy)
            fn = fobj.readline()
            arquivo = fn.decode('utf-8').replace("\r\n", '')
            self.dd.CaseFile = arquivo
            faobj = self.dz.z.open(arquivo)
            # i = -1
            # for bline in faobj.readlines():
            for i, bline in enumerate(faobj):
                # i += 1
                # line = bline.decode('utf-8')
                try:
                    line = bline.decode('utf-8')
                except Exception:
                    line = unidecode(str(bline))
                print(line)
                if i != 5:
                    continue
                fname = line[30:42].rstrip()
                functions = self.dd.functions[i]
                func = getattr(self, functions['name'])
                fobj = self.dz.z.open(fname)
                data = func(fobj)
                setattr(self.dd, functions['type'], data)

        except Exception:
            for key, value in self.dz.fns_set.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                if value.lower().split('/')[-1] == self.dd.CaseStudy:
                    fobj = self.dz.openFile(fnp=key)
                    fn = fobj.readline()
                    arquivo = fn.decode('utf-8').replace("\r\n", '')
                    self.dd.CaseFile = arquivo
                    faobj = self.dz.z.open(arquivo)
                    for bline in faobj.readlines():
                        try:
                            line = bline.decode('utf-8')
                        except Exception:
                            line = unidecode(str(bline))
                        print(line)
                    break

    def importMODIF(self, fobj):
        MODIF = dict()
        blines = fobj.readlines()
        i = 0
        while i < len(blines):
            CodUHE = blines[i].decode('utf-8').split()[0].strip()
            if int(CodUHE) > 0:
                usina = blines[i + 1].decode('utf-8')
                nome = usina[0:12].strip()
                posto = usina[12:16].strip()
                pot_inst = usina[16:22].strip()  # Valor se Newave tem NUMCNJ ou NUMMAQ ou POTEFE
                vaz_nominal = usina[22:28].strip()  # Valor se Newave tem NUMCNJ ou NUMMAQ ou POTEFE
                rend_turbger = usina[28:36].strip()
                vol_min = usina[36:44].strip()
                vol_max = usina[44:52].strip()
                u_min = usina[52:57].strip()
                cf_med = usina[57:63].strip()
                perda_h = usina[63:68].strip()
                pot_base = usina[68:74].strip()  # Potencia corresponde ao NumMinMaq para gerar ENERGIA FIRME
                cod_jus = usina[74:79].strip()
                tipo_ph = usina[79:81].strip()
                vol_min_op = usina[81:87].strip()
                usina2 = blines[i + 2].decode('utf-8')
                tipo_turb = usina2[0:2].strip()  # 1-Francis, 2-Kaplan, 3-Pelton
                fator_carga_max = usina2[2:7].strip()  # Fator para cálculo do Fator de Carga Máximo (x Cap.Efetiva = Cap.Máxima)
                volume_crista = usina2[7:13].strip()  # Volume correspondente à Crista do vertedouro (10^6 m^3)
                evaporacao = blines[i + 3].decode('utf-8').split()
                for j, v in enumerate(evaporacao):
                    evaporacao[j] = float(v)

                MODIF[int(CodUHE)] = {
                    'nome': nome,
                    'posto': int(posto),
                    'pot_inst': float(pot_inst),
                    'vaz_nominal': float(vaz_nominal),
                    'rend_turbger': float(rend_turbger),
                    'vol_min': float(vol_min),
                    'vol_max': float(vol_max),
                    'u_min': float(u_min),
                    'cf_med': float(cf_med),
                    'perda_h': float(perda_h),
                    'pot_base': float(pot_base),
                    'cod_jus': int(cod_jus),
                    'tipo_ph': int(tipo_ph),
                    'vol_min_op': float(vol_min_op),
                    'tipo_turb': int(tipo_turb),
                    'fator_carga_max': float(fator_carga_max),
                    'volume_crista': float(volume_crista),
                    'evaporacao': evaporacao
                }
            i += 4
        return MODIF

    def importDGER(self, fobj):
        DGER = dict()
        bline = fobj.readline()
        line = bline.decode('utf-8')
        DGER['tipo_estudo'] = line[0:79]
        DGER['versao_suishi'] = line[80:90]
        # for bline in fobj.readlines():
        bline = fobj.readline()
        line = bline.decode('utf-8')
        DGER['mi'] = line[0:2]  # Mês inicial para simulação
        DGER['yi'] = line[3:7]  # Ano inicial para simulação
        DGER['mf'] = line[8:10]  # Mês final para simulação
        DGER['yf'] = line[11:15]  # Ano final para simulação
        DGER['tiposim'] = line[16:17]  # Chave do tipo de simulação
        '''
                                        1: simulaçãohidrotérmica
                                        2: cálculodegarantiafísicadeenergia
                                        3: cálculodeenergiafirme,combuscadeperíodocrítico 4: cálculodeenergiafirme,comperíodocríticodefinido
        '''
        DGER['ree'] = line[18:20]  # Número de ree's para simulação
        DGER['sse'] = line[21:23]  # Número de subsistemas para simulação
        # DGER[''] = line[]  # Número de usinas do ree 1

    # def listFiles(self):
    #     return list(self.dsFileMap.keys())

    # def listRecords(self, fileType):
    #     f = self.dsFileMap.get(fileType)
    #     if f:
    #         return f.listRecords()
    #     return None

    # def setFileFilter(self, file_filter):
    #     self.file_filter = file_filter

    # def filterFile(self, f):
    #     ff = self.file_filter
    #     if ff is None:
    #         return True
    #     if f in ff:
    #         return True
    #     return False

    # def initEletBase(self):
    #     d = eletbase()
    #     self.dsFileMap['eletbase'] = d
    #     return d

    # def initEletModif(self):
    #     d = eletbase(muda=True)
    #     self.dsFileMap['eletmodif'] = d
    #     return d

    # ''' Get para importer '''
    # def get(self, fileType):
    #     return self.dsFileMap.get(fileType)

    # ''' Carrega o indice de arquivos do DESSEM '''
    # def loadIndex(self):
    #     self.loadDessem(self.getFileName('dessem.arq'))
    #     self.loadEletIndex()

    # def getFileName(self, fn):
    #     for f in os.listdir(self.dirDS):
    #         if f.lower() == fn.lower():
    #             return f

    # ''' Carrega o indice de arquivos dos dados eletricos '''
    # def loadEletIndex(self):
    #     self.loadDesselet()

    # ''' Adiciona um indice de arquivo '''
    # def addIndex(self, nome, descricao, nomeArq):
    #     self.index[nome.lower()] = {'arquivo': nomeArq, 'descricao': descricao}

    # ''' Adiciona um indice de arquivo de base de dados da rede eletrica'''
    # def addEletBaseIndex(self, cod, nome, nomeArq):
    #     self.eletIndex['base'][cod] = {'nome': nome, 'arquivo': nomeArq.replace(' ', '')} # nome do arquivo e extensao estao separados por espacos

    # ''' Adiciona um indice de arquivo de modificacao de dados da rede eletrica'''
    # def addEletModifIndex(self, cod, nome, nomeArq, codCaso, period):
    #     self.eletIndex['modif'][cod] = {'nome': nome, 'arquivo': nomeArq, 'patamar': codCaso, 'period': period}

    # '''Get para o nome de arquivo carregado pelo indice '''
    # def getArq(self, nome):
    #     if nome in self.index:
    #         return self.index[nome].get('arquivo')
    #     if nome in self.indexMap:
    #         nome = self.indexMap[nome]
    #     if nome in self.index:
    #         return self.index[nome].get('arquivo')
    #     return None

    def getLogger(self):
        return logging.getLogger(__name__)

    # def getEncoding(self):
    #     e = self.fileEncoding
    #     if not e:
    #         return [None, 'latin_1']
    #     if isinstance(e, list):
    #         return e
    #     return [e]

    # def load(self, fileType, dsFileName):
    #     lg = self.getLogger()
    #     if dsFileName is None:
    #         dsFileName = self.getArq(fileType)
    #     if dsFileName is None:
    #         lg.info('Missing index for file type: %s', str(fileType))
    #         return

    #     dsf = self.dsFileMap[fileType]
    #     fullPath = os.path.join(self.dirDS, dsFileName)
    #     for enc in self.getEncoding():
    #         try:
    #             if fileType != 'hidr':
    #                 dsf.setEncoding(enc)
    #             lg.info('Loading file: %s (%s, encoding=%s)', dsFileName, fileType, (enc if enc else 'default'))
    #             if self.file_filter:
    #                 dsf.setRecFilter(self.file_filter[fileType])
    #             dsf.clearData()
    #             dsf.readDSFile(fullPath)
    #             lg.info('File loaded successfully: %s', dsFileName)
    #             break
    #         except UnicodeDecodeError:
    #             lg.info('Exception caught, retrying loading file', exc_info=True)
    #     else:
    #         lg.error('Failed loading file: %s', fileType)

    # def loadAll(self, interval_list=None):
    #     for f in self.dsFileMap:
    #         if f not in ['dessem','eletbase','eletmodif']:
    #             if self.filterFile(f):
    #                 self.load(f, None)
    #     self.loadElet(interval_list)

    # def loadDessem(self, dsFileName):
    #     self.load('dessem', dsFileName)
    #     for r in self.get('dessem').getTable('Arq').getData():
    #         self.addIndex(r['arquivo'], r['descricao'], r['nomeArquivo'])

    # def loadDesselet(self, dsFileName=None):
    #     self.load('desselet', dsFileName)

    #     for r in self.get('desselet').getTable('Base').getData():
    #         self.addEletBaseIndex(r['idCaso'], r['nomeCaso'], r['nomeArquivo'])

    #     for r in self.get('desselet').getTable('Modif').getData():
    #         ini = datetime(r['ano'], r['mes'], r['dia'], r['hora'], r['minuto'])
    #         period = {'inicio': ini, 'duracao': r['duracao']}
    #         self.addEletModifIndex(r['periodo'], r['nomePeriodo'], r['nomeArquivo'], r['idCaso'], period)

    # def getEletBase(self, i):
    #     p = self.eletIndex['modif'][i]['patamar']
    #     return self.eletData['base'][p]

    # def getEletModif(self, i):
    #     return self.eletData['modif'][i]

    # def getEletCodList(self):
    #     return self.eletIndex['modif'].keys()

    # def getEletCodBase(self, i):
    #     r = self.eletIndex['modif'].get(i)
    #     if r is None:
    #         self.getLogger().warning('No elet base index for interval: %d', i)
    #     else:
    #         return r['patamar']

    # def getEletCodBaseSet(self, intCodList):
    #     s = set()
    #     for i in intCodList:
    #         p = self.getEletCodBase(i)
    #         if p is not None:
    #             s.add(p)
    #     return s

    # def loadElet(self, intCodList=None):
    #     if intCodList is None:
    #         intCodList = self.getEletCodList()
    #     intCodBaseList = self.getEletCodBaseSet(intCodList)

    #     if self.filterFile('eletbase'):
    #         for i in intCodBaseList:
    #             self.__loadEletBase(i)
    #     if self.filterFile('eletmodif'):
    #         for i in intCodList:
    #             self.__loadEletModif(i)

    # def __loadEletBase(self, i):
    #     r = self.eletIndex['base'].get(i)
    #     if r is None:
    #         self.getLogger().warning('eletbase: Undefined base interval: %d', i)
    #         return
    #     dsb = self.initEletBase()
    #     self.loadEletBase(r['arquivo'])
    #     self.eletData['base'][i] = dsb

    # def __loadEletModif(self, i):
    #     r = self.eletIndex['modif'].get(i)
    #     if r is None:
    #         self.getLogger().warning('eletmodif: Undefined interval: %d', i)
    #         return
    #     dsm = self.initEletModif()
    #     self.loadEletModif(r['arquivo'])
    #     self.eletData['modif'][i] = dsm

    # def loadHIDR(self, dsFileName=None):
    #     self.load('hidr', dsFileName)

    # def loadEntdados(self, dsFileName=None):
    #     self.load('entdados', dsFileName)

    # def loadOperUH(self, dsFileName=None):
    #     self.load('operuh', dsFileName)

    # def loadDadvaz(self, dsFileName=None):
    #     self.load('dadvaz', dsFileName)

    # def loadDeflant(self, dsFileName=None):
    #     self.load('deflant', dsFileName)

    # def loadEletBase(self, dsFileName=None):
    #     self.load('eletbase', dsFileName)

    # def loadEletModif(self, dsFileName=None):
    #     self.load('eletmodif', dsFileName)

    # def loadTerm(self, dsFileName=None):
    #     self.load('termdat', dsFileName)

    # def loadOperut(self, dsFileName=None):
    #     self.load('operut', dsFileName)

    # def loadPtoper(self, dsFileName=None):
    #     self.load('ptoper', dsFileName)

    # def loadAreacont(self, dsFileName=None):
    #     self.load('areacont', dsFileName)

    # def loadRespot(self, dsFileName=None):
    #     self.load('respot', dsFileName)

    # def loadCurvtviag(self, dsFileName=None):
    #     self.load('curvtviag', dsFileName)

    # def loadIlstri(self, dsFileName=None):
    #     self.load('ils_tri', dsFileName)

    # def loadCotasR11(self, dsFileName=None):
    #     self.load('cotasr11', dsFileName)

    # def loadSimul(self, dsFileName=None):
    #     self.load('simul', dsFileName)

    # def getData(self, fmt=None):
    #     dd = {}
    #     for f in self.dsFileMap:
    #         if f in ['eletbase', 'eletmodif']:
    #             continue
    #         if not self.filterFile(f):
    #             continue
    #         ds = self.dsFileMap[f]
    #         if fmt == 'dict':
    #             dd[f] = ds.toDict()
    #         else:
    #             dd[f] = ds
    #     ed = self.getEletData(fmt)
    #     for ef in ed:
    #         dd[ef] = ed[ef]
    #     return dd

    # def getEletData(self, fmt):
    #     dd = {}
    #     edb = self.eletData['base']
    #     if self.filterFile('eletbase'):
    #         dd['eletbase'] = {}
    #         for i in edb:
    #             if fmt == 'dict':
    #                 dd['eletbase'][i] = edb[i].toDict()
    #             else:
    #                 dd['eletbase'][i] = edb[i]
    #     edm = self.eletData['modif']
    #     if self.filterFile('eletmodif'):
    #         dd['eletmodif'] = {}
    #         for i in edm:
    #             if fmt == 'dict':
    #                 dd['eletmodif'][i] = edm[i].toDict()
    #             else:
    #                 dd['eletmodif'][i] = edm[i]
    #     return dd
