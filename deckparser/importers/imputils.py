

def searchInList(listobj, argsearch):
    result = dict()
    search = argsearch.strip().lower()
    for nline, vline in enumerate(listobj):
        # if svline.rfind(argsearch) != -1:
        if search in vline.strip().lower():
            result['line'] = nline
            result['value'] = vline
    return result


def getUpdateIndexes(mes_i, ano_i, mes_f, ano_f, dger):
    lista = list()
    tanoi = int(ano_i) - dger['yi']
    tmesi = int(mes_i)
    tanof = int(ano_f) - dger['yi']
    tmesf = int(mes_f)
    idx_ini = (tanoi * 12) + (12 - dger['mi']) - (12 - tmesi)
    idx_fim = (tanof * 12) + (12 - dger['mi']) - (12 - tmesf)
    if idx_ini == idx_fim:
        lista.append(idx_ini)
    else:
        lista = [x for x in range(idx_ini, idx_fim + 1)]
    return lista


def line2list(dline, mi, ar, mf, bloco, vlista=list(), dger=None):
    if len(vlista) == 0:
        vlista = [0 for i in range(dger['ni'])]
    leituras = getUpdateIndexes(mi, ar, mf, ar, dger)
    posini = (int(mi) - 1) * bloco
    for n, value in enumerate(leituras):
        posfim = posini + ((n + 1) * bloco)
        if posfim > len(dline):
            posfim = len(dline) - 1
        posinimov = posfim - bloco
        vlista[value] = float(dline[posinimov:posfim].strip())
    return vlista
