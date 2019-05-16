

def importMODIF(fobj):
    MODIF = dict()
    CodUHE = ''
    for i, rv in enumerate(fobj):
        v = rv.decode('utf-8')
        cols = v.split()
        if i > 1 and 'USINA' in v:
            CodUHE = cols[1].strip()
        elif i > 1 and v.strip() != "":
            tipo = cols[0].strip().upper()
            indice = ''
            mes = ''
            ano = ''
            if tipo == 'NUMMAQ':
                modif = [cols[1].strip(), cols[2].strip()]
            elif tipo in ['VOLMAX', 'VOLMIN']:
                modif = cols[1].strip()
                indice = cols[2].strip()
            elif tipo in ['VAZMIN', 'NUMCNJ', 'PRODESP', 'TEIF', 'IP', 'PERDHIDR', 'NUMBAS']:
                modif = cols[1]
            elif tipo in ['COEFEVAP']:
                modif = cols[1]
                mes = cols[2]
            elif tipo in ['VMAXT', 'VMINT', 'CFUGA', 'VMINP', 'VAZMINT']:
                mes = cols[1].strip()
                ano = cols[2].strip()
                modif = cols[3].strip()
                if len(cols) > 4:
                    indice = cols[4].strip()
            else:
                # NUMMAQ, POTEFE, COTAREA, VOLCOTA
                modif = ' '.join([x.strip() for x in cols[1:]])
            if CodUHE not in MODIF:
                MODIF[CodUHE] = list()
            MODIF[CodUHE].append({'tipo': tipo, 'modif': modif, 'mes': mes, 'ano': ano, 'indice': indice})
    return MODIF
