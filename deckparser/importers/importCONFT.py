def importCONFT(fobj):
    CONFT = dict()
    for i,v in enumerate(fobj):
        if (i > 1) and (v.strip() != ""):
            CodUTE = v[0:6].strip()
            nome = v[6:20].strip()
            ssis = v[20:26].strip()
            exis = v[26:33].strip()
            classe = v[33:40].strip()
            CONFT[CodUTE] = {'nome':nome,'ssis':ssis,'exis':exis,'classe':classe}
    return CONFT
