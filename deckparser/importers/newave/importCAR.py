from deckparser.importers.imputils import searchInList, getUpdateIndexes

def importCAR(fdata,dger):
    CAR = dict()
    # Inicia a leitura do arquivo caso tenha conteudo
    if len(fdata) > 0 and fdata[0].strip() != '':
        strsearch = searchInList(fdata,'CURVA DE SEGURANCA')
        if strsearch['line']:
            linerefini = int(strsearch['line'] + 3)
            strsfim = searchInList(fdata,'PROCESSO ITERATIVO')
            linereffim = int(strsfim['line'])
            for line in range(linerefini,linereffim):
                if fdata[line][0:2] == '  ' and fdata[line].strip() != '':
                    SUBSIS = fdata[line].strip()
                    curva = list()
                    curva = [ 0 for i in range(dger['ni']) ]
                elif fdata[line][0:4].strip() in str(dger['yph']):
                    # Lendo a geracao de pequenas usinas
                    anoleitura = fdata[line][0:4].strip()
                    mesini = 1
                    if anoleitura == dger['yi']:
                        mesini = dger['mi']
                    leituras = getUpdateIndexes(mesini,anoleitura,12,anoleitura,dger)
                    dados = fdata[line][6:]
                    posini = (int(mesini)-1)*6
                    for n, value in enumerate(leituras):
                        posfim = posini+((n+1)*6)
                        posinimov = posfim-6
                        curva[value] = float(dados[posinimov:posfim].strip())
                    CAR[SUBSIS] = curva
    return CAR
