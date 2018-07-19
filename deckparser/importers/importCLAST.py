def importCLAST(fobj,utes,nyears):
    CLAST = dict()
    ModifCLAST = dict()
    for i in utes:
        ModifCLAST[i] = list()
    secParte = 0
    for i,v in enumerate(fobj):
        if secParte == 0:
            if v[0:5] == " 9999":
                secParte = 1
            if (i > 1) and (v.strip() != "") and (v[0] == " ") and secParte == 0:
                CodUTE = v[0:6].strip()
                nomeclasse = v[6:19].strip()
                tipocomb = v[19:30].strip()
                tcusto = dict()
                inti = 30
                intf = 38
                for x in range(nyears):
                    tcusto[x+1] = v[inti:intf].strip()
                    inti = intf
                    intf = intf + 8
                #custo1 = v[30:38].strip()
                #custo2 = v[38:46].strip()
                #custo3 = v[46:54].strip()
                #custo4 = v[54:62].strip()
                #custo5 = v[62:70].strip()
                CLAST[CodUTE] = {'nomeclasse':nomeclasse,'tipocomb':tipocomb.upper()}
                for k,v in tcusto.iteritems():
                    CLAST[CodUTE]['custo' + str(k)] = v
                #'custo1':custo1,'custo2':custo2,'custo3':custo3,'custo4':custo4,'custo5':custo5}
        else:
            if (v[0:4] != " NUM") and (v.strip() != "") and (v[0:5] != " XXXX"):
                CodUTE = v[0:6].strip()
                custo = v[7:16].strip()
                mesi = v[17:20].strip()
                anoi = v[20:25].strip()
                mesf = v[25:29].strip()
                anof = v[29:34].strip()
                ModifCLAST[CodUTE].append({'custo':custo,'mesi':mesi,'anoi':anoi,'mesf':mesf,'anof':anof})
    return CLAST, ModifCLAST
