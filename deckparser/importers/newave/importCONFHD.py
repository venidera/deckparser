from collections import OrderedDict as odict


def importCONFHD(fobj):
    CONFHD = odict()
    for i, v in enumerate(fobj):
        vline = v.decode('utf-8')
        if vline.strip() and vline[0:5].strip() != 'NUM' and 'XXXX' not in vline:
            coduhe = vline[:5].strip()
            nome = vline[5:20].strip()
            if nome == 'BELO MONTE C':
                nome = 'B.MONTE COMP'
            # POSTO JUS   REE V.INIC U.EXIS MODIF INIC.HIST FIM HIST
            cols = vline[20:].split()
            posto = cols[0]
            jus = cols[1]
            ssis = cols[2]
            vinic = cols[3]
            uexis = cols[4]
            modif = cols[5]
            inihist = cols[6]
            fimhist = cols[7]
            desv_1 = None
            desv_2 = None
            try:
                desv_1 = cols[8]
                desv_2 = cols[9]
                # posto = vline[20:26].strip()
                # jus = vline[26:31].strip()
                # ssis = vline[31:36].strip()
                # vinic = vline[35:43].strip()
                # uexis = vline[42:49].strip()
                # modif = vline[48:56].strip()
                # inihist = vline[55:64].strip()
                # fimhist = vline[64:73].strip()
                # desv_1 = None
                # desv_2 = None
                # try:
                #     if len(vline) > 73:
                #         desv_1 = vline[72:78].strip()
                #         desv_2 = vline[78:].strip()
            except Exception as e:
                pass
            CONFHD[coduhe] = {
                'nome': nome,
                'posto': posto,
                'jus': jus,
                'ssis': ssis,
                'vinic': vinic,
                'uexis': uexis,
                'modif': modif,
                'inihist': inihist,
                'fimhist': fimhist,
                'desv_1': desv_1,
                'desv_2': desv_2}
    return CONFHD
