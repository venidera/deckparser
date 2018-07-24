def importEXPT(fobj,utes):
    EXPT = dict()
    for i in utes:
        EXPT[i] = list()
    for i,v in enumerate(fobj):
        if (i > 1) and (v.strip() != "") and (v[0] == " "):
            CodUTE = v[0:4].strip()
            tipo = v[5:11].strip()
            modif = v[12:20].strip()
            mi = v[20:23].strip()
            anoi = v[23:28].strip()
            mf = v[28:31].strip()
            anof = v[31:36].strip()
            EXPT[CodUTE].append({'tipo':tipo,'modif':modif,'mi': mi,'anoi':anoi,'mf':mf,'anof':anof})
    return EXPT
