def importEXPH(fdata):
    ENCHVM = dict()
    MOTORI = dict()
    cline = 3
    while cline < len(fdata):
        coduhe = fdata[cline][0:5].strip()
        nome = fdata[cline][5:18].strip()
        if fdata[cline][17:43].strip():
            # Enchimento de Volume Morto
            iniench = fdata[cline][17:26].strip()
            durmeses = fdata[cline][26:36].strip()
            pct = fdata[cline][36:43].strip()
            cline = cline + 1
            ENCHVM[coduhe] = {'nome': nome, 'iniench': iniench,
                              'durmeses': durmeses, 'pct': pct}
        else:
            ENCHVM[coduhe] = {'nome': nome, 'iniench': None,
                              'durmeses': None, 'pct': None}
        if fdata[cline].strip() == '9999':
            cline = cline + 1
            continue
        # Motorizacao
        MOTORI[coduhe] = list()
        while fdata[cline].strip() != '9999':
            # loop no bloco
            maq = None
            conj = None
            if len(fdata[cline]) > 61:
                # Formato novo, entao informa nro de maq e do cnj
                # if fdata[cline][:4].strip() == '':
                if '(' in fdata[cline]:
                    portion = fdata[cline].split('(')[1].split(')')[0].split()
                    maq = int(portion[0])
                    conj = int(portion[1])
                else:
                    maq = int(fdata[cline][59:62].strip().replace('(', ''))
                    conj = int(fdata[cline][62:].strip())
            dataexp = fdata[cline][33:51].strip()
            potexp = fdata[cline][51:59].strip()
            MOTORI[coduhe].append({'data': dataexp, 'pot': potexp,
                                   'nome': nome, 'maq': maq, 'conj': conj})
            cline = cline + 1
    return ENCHVM, MOTORI
