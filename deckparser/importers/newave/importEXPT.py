def importEXPT(fobj,utes):
    EXPT = dict()
    for i in utes:
        EXPT[i] = list()
    for i,v in enumerate(fobj):
        if (i > 1) and (v.strip() != ""):
            CodUTE = v[0:4].decode('utf-8').strip()
            tipo = v[5:11].decode('utf-8').strip()
            modif = v[12:20].decode('utf-8').strip()
            mi = v[20:23].decode('utf-8').strip()
            anoi = v[23:28].decode('utf-8').strip()
            mf = v[28:31].decode('utf-8').strip()
            anof = v[31:36].decode('utf-8').strip()
            EXPT[CodUTE].append({'tipo':tipo,'modif':modif,'mi': mi,'anoi':anoi,'mf':mf,'anof':anof})
    return EXPT
