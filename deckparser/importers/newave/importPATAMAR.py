from deckparser.importers.imputils import line2list, searchInList


def importPATAMAR(fdata, dger, sss):
    # Inicia a leitura do arquivo
    # Verificar o numero de patamares de carga
    idxline = 2
    numpatamarcarga = int(fdata[idxline].strip())
    # Ler duracao dos patamares
    idxline = 6
    PATDURA = dict()
    PATCARGA = dict()
    PATINTER = list()
    PATNSIM = dict()  # multiplicadores das usinas não simuladas
    if numpatamarcarga == 1:
        PATDURA[0] = [1.0] * dger['ni']
    else:
        for i in range(numpatamarcarga):
            PATDURA[i] = list()
        for idss in sss:
            PATCARGA[idss] = dict()
            for i in range(numpatamarcarga):
                PATCARGA[idss][i] = list()
        for _anoi in range(dger['nyears']):
            if fdata[idxline][0:5].strip() in str(dger['yph']):
                anopat = fdata[idxline][0:5].strip()
                for idpat in range(numpatamarcarga):
                    # Lendo os valores
                    mesini = 1
                    if int(anopat) == dger['yi']:
                        mesini = dger['mi']
                    PATDURA[idpat] = line2list(dline=fdata[idxline][5:102],
                                               mi=mesini, ar=anopat, mf=12,
                                               bloco=8, vlista=PATDURA[idpat],
                                               dger=dger)
                    idxline = idxline + 1
    # Carregar os patamares de carga
    idxline = searchInList(fdata, 'CARGA(P.U.DEMANDA MED.)')['line'] + 2
    for idxss in sss:
        ssis = int(fdata[idxline].strip())
        if numpatamarcarga == 1:
            PATCARGA[str(ssis)] = [[1.0] * dger['ni']]
            continue
        if int(idxss) == ssis:
            idxline = idxline + 1
            for _anoi in range(dger['nyears']):
                if fdata[idxline][0:8].strip() in str(dger['yph']):
                    anopat = fdata[idxline][0:8].strip()
                    for idpat in range(numpatamarcarga):
                        # Lendo os valores
                        mesini = 1
                        if int(anopat) == dger['yi']:
                            mesini = dger['mi']
                        PATCARGA[str(ssis)][idpat] = line2list(
                            dline=fdata[idxline][7:91], mi=mesini, ar=anopat,
                            mf=12, bloco=7, vlista=PATCARGA[str(ssis)][idpat],
                            dger=dger)
                        idxline = idxline + 1

    idxline = searchInList(fdata, 'INTERCAMBIO(P.U.INTERC.MEDIO)')['line'] + 2
    while len(fdata[idxline].strip()) > 0 and numpatamarcarga > 1:
        vals = fdata[idxline].split()
        # if fdata[idxline][0:2].strip() == '' and fdata[idxline][0:5].strip() != '':
        if len(vals) == 2:
            ori, des = vals
            # ori = fdata[idxline][0:5].strip()
            # des = fdata[idxline][5:8].strip()
            PATINTER.append({'ORI': ori, 'DES': des,
                             'pat1': list(), 'pat2': list(), 'pat3': list(),
                             'pat4': list(), 'pat5': list(), 'pat6': list()})
            idxline = idxline + 1
            for _anoi in range(dger['nyears']):
                if fdata[idxline][0:8].strip() in str(dger['yph']):
                    anopat = fdata[idxline][0:8].strip()
                    for idpat in range(numpatamarcarga):
                        # Lendo os valores
                        mesini = 1
                        if int(anopat) == dger['yi']:
                            mesini = dger['mi']
                        PATINTER[len(PATINTER) - 1]['pat' + str(idpat + 1)] =\
                            line2list(dline=fdata[idxline][7:91],
                                      mi=mesini, ar=anopat,
                                      mf=12, bloco=7,
                                      vlista=PATINTER[len(PATINTER) - 1][
                                          'pat' + str(idpat + 1)],
                                      dger=dger)
                        idxline = idxline + 1
        elif len(vals) == 1 and vals[0] == '9999':
            break
        if idxline >= len(fdata):
            break

    idx = searchInList(fdata,
        'BLOCO DE USINAS NAO SIMULADAS (P.U. ENERGIA MEDIA)')
    if idx == {}:
        idx = searchInList(fdata,
            'BLOCO DE USINAS NAO SIMULADAS (P.U. MONTANTE MED.)')

    idxline = idx['line'] + 2 if idx else None
    for idss in sss:
        PATNSIM[idss] = dict()
        for i in range(numpatamarcarga):
            PATNSIM[idss][i] = {
                'bloco01': [],
                'bloco02': [],
                'bloco03': [],
                'bloco04': [],
                'bloco05': [],
                'bloco06': [],
                'bloco07': [],
                'bloco08': [],
                'bloco09': [],
                'bloco10': []
                }

    if idxline:
        while len(fdata[idxline].strip()) > 0 and numpatamarcarga > 1:
            vals = fdata[idxline].split()

            if len(vals) == 2:
                subsis, bloc = vals
                idxline = idxline + 1

                for _anoi in range(dger['nyears']):
                    anopat = fdata[idxline][0:8].strip()
                    if anopat in str(dger['yph']):
                        for idpat in range(numpatamarcarga):
                            # Lendo os valores
                            mesini = 1
                            if int(anopat) == dger['yi']:
                                mesini = dger['mi']
                            PATNSIM[subsis][idpat]['bloco0'+str(bloc)] =\
                                line2list(dline=fdata[idxline][7:91],
                                          mi=mesini,
                                          ar=anopat,
                                          mf=12,
                                          bloco=7,
                                          vlista=PATNSIM[subsis][idpat][
                                              'bloco0'+str(bloc)],
                                          dger=dger)
                            idxline = idxline + 1
            elif len(vals) == 1 and vals[0] == '9999':
                break
            if idxline >= len(fdata):
                break

    return PATDURA, PATCARGA, PATINTER, PATNSIM, numpatamarcarga

