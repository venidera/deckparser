def importMANUTT(fobj,utes):
    MANUTT = dict()
    for i in utes:
        MANUTT[i] = list()
    for i,v in enumerate(fobj):
        if (i > 1) and (v.strip() != ""):
            CodUTE = v[17:20].strip()
            nome = v[20:35].strip()
            unidtermica = v[38:40].strip()
            data = v[40:49].strip()
            dia = data[0:2]
            mes = data[2:4]
            ano = data[4:8]
            dur = v[49:53].strip()
            pot = v[55:64].strip()
            MANUTT[CodUTE].append({'nome':nome,'unidtermica':unidtermica,'data':data,'dia':dia,'mes':mes,'ano':ano,'dur':dur,'pot':pot})
    return MANUTT    
