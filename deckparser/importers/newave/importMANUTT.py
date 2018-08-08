

def importMANUTT(fobj, utes):
    MANUTT = dict()
    for i in utes:
        MANUTT[i] = list()
    for i, v in enumerate(fobj):
        if (i > 1) and (v.strip() != ""):
            CodUTE = v[17:20].strip()
            nome = v[20:35].strip()
            unidtermica = v[38:40].strip()
            data = v[40:49].strip()
            dia = data[0:2].strip()
            mes = data[2:4].strip()
            ano = data[4:8].strip()
            dur = v[49:53].strip()
            pot = v[55:64].strip()
            MANUTT[CodUTE.decode('utf-8')].append(
                {'nome': nome.decode('utf-8'),
                 'unidtermica': unidtermica.decode('utf-8'),
                 'data': data.decode('utf-8'),
                 'dia': dia.decode('utf-8'),
                 'mes': mes.decode('utf-8'),
                 'ano': ano.decode('utf-8'),
                 'dur': dur.decode('utf-8'),
                 'pot': pot.decode('utf-8')})
    return MANUTT
