
from deckparser.importers.imputils import searchInList, getUpdateIndexes
from collections import OrderedDict as odict


def importSISTEMA(fdata,dger):
    SISTEMA = odict()
    # Inicia a leitura do arquivo
    # Ler numero de patamares de deficit
    strsearch = searchInList(fdata, 'NUMERO DE PATAMARES DE DEFICIT')
    if strsearch['line']:
        SISTEMA['npdef'] = int(fdata[strsearch['line'] + 2])
    # Ler lista de subsistemas reais, sem ficticios
    #SISTEMA['ss'] = list(['SIN'])
    SISTEMA['sss'] = odict()
    strsearch = searchInList(fdata, ' NUM|NOME SSIS.|')
    if strsearch['line']:
        lineref = int(strsearch['line'] + 2)
        while True:
            fict = int(fdata[lineref][16:19].strip())
            name = fdata[lineref][5:16].strip()
            cod = fdata[lineref][0:4].strip()
            SISTEMA['sss'][cod] = { 'name':name, 'fict': fict }
            lineref += 1
            if fdata[lineref][0:4].strip() == '999':
                break
    # Ler Custo de Deficit
    SISTEMA['deficit'] = odict()
    for i in SISTEMA['sss'].keys():
        if SISTEMA['sss'][i]['fict'] == 0:
            SISTEMA['deficit'][int(i)] = odict()
    strsearch = searchInList(fdata,'CUSTO DO DEFICIT')
    if strsearch['line']:
        line = int(strsearch['line'] + 3)
        while fdata[line][0:4].strip() != '999':
            ssis = int(fdata[line][0:3].strip())
            if SISTEMA['sss'][str(ssis)]['fict'] == 0:
                defpat1 = fdata[line][19:27].strip()
                defpat2 = fdata[line][27:35].strip()
                defpat3 = fdata[line][35:43].strip()
                defpat4 = fdata[line][43:51].strip()
                pucortepat1 = fdata[line][51:57].strip()
                pucortepat2 = fdata[line][57:63].strip()
                pucortepat3 = fdata[line][63:69].strip()
                pucortepat4 = fdata[line][69:75].strip()
                SISTEMA['deficit'][ssis] = {'defpat1':defpat1,'defpat2':defpat2,'defpat3':defpat3,'defpat4':defpat4,'pucortepat1':pucortepat1,'pucortepat2':pucortepat2,'pucortepat3':pucortepat3,'pucortepat4':pucortepat4}
            line += 1
    # Ler limites de intercambio
    SISTEMA['liminter'] = list()
    strsearch = searchInList(fdata,'LIMITES DE INTERCAMBIO')
    if strsearch['line']:
        linerefini = int(strsearch['line'] + 3)
        strsfim = searchInList(fdata,'MERCADO DE ENERGIA TOTAL')
        linereffim = int(strsfim['line'] - 1)
        yearsload = 0
        for line in range(linerefini,linereffim):
            #if fdata[line][0:2] == '  ' and fdata[line].strip() != '':
            if fdata[line].strip() != '' and int(fdata[line].split()[0]) < 1900:
                IORI = fdata[line].split()[0]
                IDES = fdata[line].split()[1]
                limites = list()
                limites = [ 0 for i in range(dger['ni']) ]
            #elif fdata[line][0:4].strip() != '' and int(fdata[line][0:4].strip()) in dger['yph']:
            elif fdata[line][0:4].strip() != '' and int(fdata[line].split()[0]) in dger['yph']:
            # Lendo fluxo entre as duas pontas
                anoleitura = int(fdata[line][0:4].strip())
                mesini = 1
                if anoleitura == dger['yi']:
                    mesini = dger['mi']
                leituras = getUpdateIndexes(mesini,anoleitura,12,anoleitura,dger)
                dados = fdata[line][7:]
                posini = (int(mesini)-1)*8
                for n, value in enumerate(leituras):
                    posfim = posini+((n+1)*8)
                    posinimov = posfim-8
                    limites[value] = float(dados[posinimov:posfim].strip())
                yearsload = yearsload + 1
                if yearsload == dger['nyears']:
                    SISTEMA['liminter'].append({'ORI':IORI, 'DES':IDES, 'limites':limites})
                    vtemp = IORI
                    IORI = IDES
                    IDES = vtemp
                    limites = list()
                    limites = [ 0 for i in range(dger['ni']) ]
                    yearsload = 0
    # Ler o mercado total de energia por subsistema
    if strsfim['line']:
        linerefini = int(strsfim['line'] + 3)
        strsfim = searchInList(fdata,'GERACAO DE PEQUENAS USINAS')
        if len(strsfim) == 0:
            strsfim = searchInList(fdata,'GERACAO DE USINAS NAO SIMULADAS')
        linereffim = int(strsfim['line'] - 1)
        SISTEMA['mercado'] = odict()
        #for i in SISTEMA['sss'].keys():
        #    if SISTEMA['sss'][i]['fict'] == 0:
        #    SISTEMA['mercado'][i] = dict()
        for line in range(linerefini,linereffim):
            if fdata[line][0:2] == '  ' and fdata[line].strip() != '':
                SUBSIS = fdata[line][0:12].strip()
                demanda = list()
                demanda = [ 0 for i in range(dger['ni']) ]
                pos = list()
                pos = [ 0 for i in range(1,13) ]
            elif fdata[line][0:4].strip() in str(dger['yph']):
                # Lendo mercado
                anoleitura = fdata[line][0:4].strip()
                mesini = 1
                if anoleitura == dger['yi']:
                    mesini = dger['mi']
                leituras = getUpdateIndexes(mesini,anoleitura,12,anoleitura,dger)
                dados = fdata[line][7:]
                posini = (int(mesini)-1)*8
                for n, value in enumerate(leituras):
                    if value >= 0:
                        posfim = posini+((n+1)*8)
                        posinimov = posfim-8
                        demanda[value] = float(dados[posinimov:posfim].strip())
            elif fdata[line][0:3].strip() == 'POS':
                dados = fdata[line][7:]
                for n in range(0,12):
                    posfim = ((n+1)*8)
                    posinimov = posfim-8
                    pos[n] = float(dados[posinimov:posfim].strip())
                SISTEMA['mercado'][SUBSIS] = {'demanda':demanda, 'pos':pos}
    # Ler a geracao de pequenas usinas
    if strsfim['line']:
        linerefini = int(strsfim['line'] + 3)
        linereffim = len(fdata) - 1
        SISTEMA['gpu'] = odict()
        for line in range(linerefini,linereffim):
            if fdata[line][0:2] == '  ' and fdata[line].strip() != '':
                SUBSIS = fdata[line].strip()
                pequ = list()
                pequ = [ 0 for i in range(dger['ni']) ]
            elif fdata[line].strip() == '999':
                break
            elif int(fdata[line][0:4].strip()) in dger['yph']:
                # Lendo a geracao de pequenas usinas
                anoleitura = int(fdata[line][0:4].strip())
                mesini = 1
                if anoleitura == dger['yi']:
                    mesini = dger['mi']
                leituras = getUpdateIndexes(mesini,anoleitura,12,anoleitura,dger)
                dados = fdata[line][7:]
                posini = (int(mesini)-1)*8
                for n, value in enumerate(leituras):
                    posfim = posini+((n+1)*8)
                    posinimov = posfim-8
                    pequ[value] = float(dados[posinimov:posfim].strip())
                SISTEMA['gpu'][SUBSIS] = pequ
    return SISTEMA
