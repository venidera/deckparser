

def importCADIC(fdata, dger):
    CADIC = dict()
    # Indexador de linha em leitura
    liner = 2
    impc = -1
    if len(fdata) > 0:
        while fdata[liner].strip() != '999':
            vcheck = fdata[liner][:4].strip()
            if 0 < len(vcheck) < 4 and 'PRE' != vcheck and 'POS' != vcheck:
                vals = fdata[liner].split()
                subsis = vals[0]
                if subsis not in CADIC.keys():
                    CADIC[subsis] = dict()
                pt1 = vals[1]
                if len(vals) > 2:
                    pt2 = vals[2]
                else:
                    pt2 = ''
                liner += 1
                impc += 1
            else:
                ano = fdata[liner][:4].strip()
                # PRE ainda será tratado
                if ano == '' or len(fdata[liner].strip()) <= 4:
                    # PDE ou Leilao - Sem C_ADIC
                    valores = [0.0] * dger['ni']
                    CADIC[subsis][impc] = {'pt1': pt1, 'pt2': pt2, 'valores': valores.copy()}
                    while fdata[liner][:4].strip() == '' or len(fdata[liner].strip()) <= 4 and fdata[liner].strip() != '999':
                        liner += 1
                    continue
                elif len(ano) == 4 and ano in str(dger['yph']):
                    # Lendo os valores
                    lvals = fdata[liner][7:].split()
                    if int(ano) == dger['yi'] and dger['mi']>1 and len(lvals)==12:
                        valores = lvals[dger['mi'] - 1:]
                    else:
                        valores = lvals
                if impc not in CADIC[subsis]:
                    CADIC[subsis][impc] = {'pt1': pt1, 'pt2': pt2, 'valores': valores}
                else:
                    CADIC[subsis][impc]['valores'] += valores.copy()
                liner = liner + 1
    return CADIC
