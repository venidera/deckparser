def importCONFHD(fobj):
    CONFHD = dict()
    for i, v in enumerate(fobj):
        vline = v.decode('utf-8')
        if vline.strip() and vline[0:5].strip() != 'NUM' and 'XXXX' not in vline:
            cols = vline.split()
            coduhe = cols[0].strip()
            nome = cols[1].strip()
            if nome == 'BELO MONTE C':
                nome = 'B.MONTE COMP'
            posto = cols[2].strip()
            jus = cols[3].strip()
            ssis = cols[4].strip()
            vinic = cols[5].strip()
            uexis = cols[6].strip()
            modif = cols[7].strip()
            inihist = cols[8].strip()
            fimhist = cols[9].strip()
            CONFHD[coduhe] = {
                'nome': nome,
                'posto': posto,
                'jus': jus,
                'ssis': ssis,
                'vinic': vinic,
                'uexis': uexis,
                'modif': modif,
                'inihist': inihist,
                'fimhist': fimhist}
    return CONFHD
