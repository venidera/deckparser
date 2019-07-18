# from logging import info

# Chaves do MODIF Processadas:
# VOLMIN   : ok
# VOLMAX   : ok
# VAZMIN   : ok
# NUMCNJ   : ok
# NUMMAQ   : ok
# POTEFE   : ok
# PRODESP  : ok
# TEIF     : ok
# IP       : ok
# PERDHIDR : ok
# COEFEVAP : ok
# COTAAREA : ok
# VOLCOTA  : ok
# CFUGA    : ok
# VMAXT    : ok
# VMINT    : ok
# NUMBAS   : ok
# VMINP    : nao tratado
# VAZMINT  : ok


class SuishiDicted(object):
    def __init__(self):
        # Arquivo do Caso
        self.CaseStudy = 'caso.dat'  # Nome do arquivo que contém o nome dos arquivos de entrada utilizados pelo modelo SUISHI.
        self.CaseFile = 'arquivo.eas'  # Nome dos Arquivos Utilizados pelo Programa
        # Nomes contidos no arquivo, formato A12 a partir da coluna 31
        self.functions = [
            {'type': 'DGER', 'name': 'importDGER'},  # dger.eas - ARQUIVO DE DADOS GERAIS,
            {'type': 'SISTEMA', 'name': 'importSISTEMA'},  # sistema.eas - ARQUIVO DADOS DOS SUBSISTEMA
            {'type': 'CONFH', 'name': 'importCONFH'},  # confh.eas - ARQUIVO CONFIG HIDROELETRICA
            {'type': 'TERM', 'name': 'importTERM'},  # term.eas - ARQUIVO CONFIGURACAO TERMICA
            {'type': 'CLAST', 'name': 'importCLAST'},  # clast.eas - ARQUIVO DADOS CLASSES TERMIC
            {'type': 'MODIF', 'name': 'importMODIF'}  # modif55.eas - ARQUIVO ALTERACAO USIN HIDRO
            #     'EXPANSAO': 'expansao.eas',  # ARQUIVO EXPANSAO HIDROTERMIC
            #     'VAZOES': 'vazoes.dat',  # ARQUIVO DE VAZOES
            #     'POSTOS': 'postos.dat',  # ARQUIVO DE POSTOS
            #     'HIDR': 'hidr.dat',  # ARQUIVO DADOS USINAS HIDRO
            #     'DSVAGUA': 'dsvagua.eas',  # ARQUIVO USOS ALTERNATIVOS
            #     'CORTESH': 'cortesh.eas'  # ARQUIVO AUXILIAR DA FCF
            #     'CORTES' 'cortes.eas',  # ARQUIVO FUNCAO CUSTO FUTURO
            #     'NEWDESP': 'newdesp.eas',  # ARQUIVO NEWAVE DADOS CONFIG
            #     'SHP': 'shp.eas',  # ARQUIVO INPUT SIMUL PARAIBA
            #     'PEQUSI': 'pequsi.eas',  # ARQUIVO PEQUENAS USINAS
            #     'PATAMAR': 'patamar.eas',  # ARQUIVO DE PATAMARES MERCADO
            #     'EAFPAST': 'eafpast.mlt',  # ARQUIVO C/TEND. HIDROLOGICA
            #     'ITAIPU': 'itaipu.dat',  # ARQUIVO RESTRICAO ITAIPU
            #     'BID': 'bid.dat',  # ARQUIVO DEMAND SIDE BIDDING
            #     'C_ADIC': 'c_adic.dat',  # ARQUIVO CARGAS ADICIONAIS
            #     'LOSS': 'loss.dat',  # ARQUIVO PERDA DE TRANSMISSAO
            #     'SUISHI_REL': 'suishi.rel',  # ARQUIVO RELATORIO
            #     'DIRETOR': 'diretor.csv',  # ARQUIVO RESUMO OPER MENSAL
            #     'SUBSIS': 'subsis.csv',  # ARQUIVO RESUMO SUBSISTEMA
            #     'USIHID': 'usihid.csv',  # ARQUIVO RESUMO USI HIDROELET
            #     'USITER': 'usiter.csv',  # ARQUIVO RESUMO USI TERMICA
            #     'PBSUISHI': 'pbsuishi.csv',  # ARQUIVO OUTPUT PARAIBA SUL
            #     'PDISP': 'pdisp.dat',  # ARQUIVO POTENCIA CONFIABILID
            #     'GTMINPAT': 'gtminpat.dat',  # ARQUIVO FATOR G.TERMICA MIN.
            #     'ATIETE': 'atiete.dat',  # ARQUIVO PAR. ALTO TIETE
            #     'CURVA_ARM': 'curva.eas',  # ARQUIVO PAR. CURVA ARM MIN
            #     'GERTER': 'gerter.csv',  # ARQUIVO GER. TERM. / CLASSE
            #     'INTER': 'inter.csv',  # ARQUIVO DE INTERCAMBIOS
            #     'EFGA': 'efga.csv',  # ARQUIVO ENERGIA FIRME/ASSEG
            #     'ADTERM': 'adterm.dat',  # ARQUIVO DESP. TERM. ANTEC.
            #     'SAR': 'sar.dat',  # ARQUIVO AVERSAO A RISCO SAR
            #     'CVAR': 'cvar.dat',  # ARQUIVO AVERSAO A RISCO CVAR
            #     'CGUIAOP': 'cguiaop.dat',  # ARQUIVO CURVA GUIA DE OPER.
            #     'VMAXTSAZ': 'vmaxtsaz.dat',  # ARQUIVO VMAXT SAZONAL - E.F.
            #     'VAZMINTO': 'vazmintp.dat',  # ARQUIVO VAZMINT PERIODO PRE
            #     'REE_DADOS': 'ree.dat',  # ARQUIVO DE DADOS RES EQUIV
            #     'REE_RESUMO': 'ree.csv',  # ARQUIVO RESUMO RESV EQUIVAL
            # }
        ]
        # Dados de sistema e problema
        self.DGER = None
        # self.SISTEMA = None
        # self.CAR = None
        # self.CADIC = None
        # self.PATDURA = None
        # self.PATCARGA = None
        # self.PATINTER = None

        # # Dados do parque termelétrico
        # self.TERM = None
        # self.CONFT = None
        # self.CADTERM = None
        # self.EXPT = None
        # self.CLAST = None
        # self.MODIFCLAST = None
        # self.MANUTT = None

        # # Dados do parque hidrelétrico
        # self.CONFHD = None
        # self.HIDR = None
        # self.HIDRcount = None
        self.MODIF = None
        # self.DSVAGUA = None
        # self.VAZOES = None

        # self.VAZcount = None
        # self.VAZMAX = None

        # self.ENCHVM = None
        # self.MOTORI = None

        # self.REE = None
        # self.REElabels = None

        # # Helpers
        # self.nss = None
        # self.sss = None
        # self.ssname = None
        # self.ssfict = None
