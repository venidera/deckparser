def importCADTERM(fobj):
    CADTERM = dict()
    for i,rv in enumerate(fobj):
        v = rv.decode('utf-8')
        if (i > 1) and (v.strip() != "") and 'NUM' not in v and 'XXXXX' not in v:
            sstr = len(v[0:6].strip())
            if sstr == 3:
                # Linha de codigo de UTE - Tem zeros
                codute = str(int(v[0:6].strip()))
            elif sstr == 6:
                if codute not in CADTERM.keys():
                    CADTERM[codute] = 1
                else:
                    CADTERM[codute] += 1
    return CADTERM
