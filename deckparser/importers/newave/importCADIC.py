from deckparser.importers.imputils import line2list


def importCADIC(fdata, dger):
    CADIC = dict()
    # Indexador de linha em leitura
    liner = 2
    impc = -1
    while fdata[liner].strip() != '999':
        if len(fdata[liner].strip()) < 100:
            subsis = fdata[liner][0:6].strip()
            pt1 = fdata[liner][6:20].strip()
            pt2 = fdata[liner][20:32].strip()
            liner += 1
            impc += 1
            valores = list()
        ano = fdata[liner][0:4].strip()
        if ano == '':
            # nao informa ano: encontrado em deck PDE
            ano = '0000'
        if ano in str(dger['yph']):
            # Lendo os valores
            if int(ano) == dger['yi']:
                mesini = dger['mi']
            else:
                mesini = 1
            # Leitura dos valores
            valores = line2list(dline=fdata[liner][7:103], mi=mesini, ar=ano, mf=12, bloco=8, vlista=valores, dger=dger)
            if subsis not in CADIC.keys():
                CADIC[subsis] = dict()
            CADIC[subsis][impc] = {'pt1': pt1, 'pt2': pt2, 'valores': valores}
        liner = liner + 1
    return CADIC
