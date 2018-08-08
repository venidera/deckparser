
def importTERM(fobj):
    TERM = dict()
    for i, v in enumerate(fobj):
        if (i > 1) and (v.strip() != ""):
            CodUTE = v[0:4].decode('utf-8').strip()
            nome = v[5:18].decode('utf-8').strip()
            pot = v[19:24].decode('utf-8').strip()
            fcmax = v[25:30].decode('utf-8').strip()
            teif = v[31:38].decode('utf-8').strip()
            ip = v[39:45].decode('utf-8').strip()
            gtmin1 = v[45:52].decode('utf-8').strip()
            gtmin2 = v[52:59].decode('utf-8').strip()
            gtmin3 = v[59:66].decode('utf-8').strip()
            gtmin4 = v[66:73].decode('utf-8').strip()
            gtmin5 = v[73:80].decode('utf-8').strip()
            gtmin6 = v[80:87].decode('utf-8').strip()
            gtmin7 = v[87:94].decode('utf-8').strip()
            gtmin8 = v[94:101].decode('utf-8').strip()
            gtmin9 = v[101:108].decode('utf-8').strip()
            gtmin10 = v[108:115].decode('utf-8').strip()
            gtmin11 = v[115:122].decode('utf-8').strip()
            gtmin12 = v[122:129].decode('utf-8').strip()
            gtdmais = v[129:137].decode('utf-8').strip()
            TERM[CodUTE]={
                'nome': nome,
                'pot': pot,
                'fcmax': fcmax,
                'teif': teif,
                'ip': ip,
                'gtmin1': gtmin1,
                'gtmin2': gtmin2,
                'gtmin3': gtmin3,
                'gtmin4': gtmin4,
                'gtmin5': gtmin5,
                'gtmin6': gtmin6,
                'gtmin7': gtmin7,
                'gtmin8': gtmin8,
                'gtmin9': gtmin9,
                'gtmin10': gtmin10,
                'gtmin11': gtmin11,
                'gtmin12': gtmin12,
                'gtdmais': gtdmais}
    return TERM
