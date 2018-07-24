
def importMODIF(fobj,uhes):
    MODIF = dict()
    for i in uhes:
        MODIF[i] = list()
    CodUHE = ''
    for i,rv in enumerate(fobj):
        v = rv.decode('utf-8')
        if (i > 1) and (v.strip() != "") and (v[0:9].strip() == 'USINA'):
            CodUHE = str(int(v[9:31].strip()))
        elif (i > 1) and (v.strip() != ""):
            tipo = v[0:9].strip()
            #if tipo == 'VOLMAX':
            #    print 'ESTE EH VOLMAX'
            #    print 'LEN(V) :', len(v)
            if len(v) <= 22:
                indice = ''
                if tipo == 'NUMMAQ':
                    modif = [ v[9:14].strip() , v[14:].strip() ]
                elif tipo == 'VOLMAX' or tipo == 'VOLMIN':
                    #print 'VOLMAX'
                    modif = v[8:17].strip()
                    indice = v[17:20].strip()
                    #print 'MODIF: ', modif
                    #print 'INDICE: ', indice
                else:
                    modif = v[9:31].strip()
                mes = ''
                ano = ''
            else:
                mes = v[9:13].strip()
                ano = v[13:18].strip()
                modif = v[18:26].strip()
                indice = v[26:31].strip()
            MODIF[CodUHE].append({'tipo':tipo,'modif':modif,'mes': mes,'ano':ano,'indice':indice})
    return MODIF
