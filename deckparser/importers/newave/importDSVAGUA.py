from deckparser.importers.imputils import line2list


def importDSVAGUA(fdata, uhes, dger, decktype=False):
    DSVAGUA = dict()
    for i in uhes:
        DSVAGUA[i] = [0.0] * dger['ni']
    cline = 2
    tipo = ''
    valores = [0.0] * dger['ni']
    inicio = 0
    while fdata[cline].strip() != '9999':
        # print 'fdata[cline] = ',fdata[cline]
        ano = fdata[cline][0:4].strip()
        if ano in str(dger['yph']):
            CodUHE = fdata[cline][5:9].strip()
            # Verificar se eh linha de tipagem, se nao for vai seguir com o tipo anterior.
            if len(fdata[cline]) > 104:
                # linha de tipo
                valores = list()
                tipo = fdata[cline][102:120].strip()
                if (tipo == 'Usos_Consuntivos'):
                    txttipo = 'usocon'
                else:
                    txttipo = 'vazrem'
            if int(ano) == dger['yi']:
                mesini = dger['mi']
            else:
                mesini = 1
            valores = line2list(dline=fdata[cline][9:95], mi=mesini, ar=ano,
                                mf=12, bloco=7, vlista=valores, dger=dger)
            if ano == str(dger['yph'][-1]):
                DSVAGUA[CodUHE] = list(
                    map(sum, zip(DSVAGUA[CodUHE], valores)))
        cline += 1
    return DSVAGUA
