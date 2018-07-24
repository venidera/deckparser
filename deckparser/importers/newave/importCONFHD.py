def importCONFHD(fobj):
    CONFHD = dict()
    for i,v in enumerate(fobj):
        if v[0:5].strip() != 'NUM' and v[0:5].strip() != 'XXXX' and v.strip() != '':
            CodUHE = v[0:5].strip()
            nome = v[5:19].strip()
            if nome == 'BELO MONTE C':
                nome = 'B.MONTE COMP'
            posto = v[19:24].strip()
            jus = v[25:31].strip()
            ssis = v[31:35].strip()
            vinic = v[35:43].strip()
            uexis = v[44:48].strip()
            modif = v[49:55].strip()
            inihist = v[55:64].strip()
            fimhist = v[65:72].strip()
            # Nao inclui UHE marcada com Existencia = NC
            if uexis is 'NC':
                info('UHE ignored - CodUHE: '+str(CodUHE)+'  Name: '+str(nome))
                info('-------------------------------')
            else:
                CONFHD[CodUHE]={'nome':nome,'posto':posto,'jus':jus,'ssis':ssis, 'vinic':vinic,'uexis':uexis,'modif':modif,'inihist':inihist,'fimhist':fimhist}
    return CONFHD
