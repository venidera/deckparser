from unidecode import unidecode
import re

def importDGER(fobj):
    DGER = dict()
    DGER['info'] = None
    for bline in fobj.readlines():
        try:
            line = bline.decode('utf-8')
        except:
            line = unidecode(str(bline))
        if not DGER['info']:
            DGER['info'] = unidecode(str(line)).strip().replace("b'",'').replace('\\xe3','a').replace("\\r\\n'",'')
        elif line.rfind('TIPO DE EXECUCAO') != -1:
            DGER['tipoexec'] = int(line[21:25].strip())
        elif line.rfind('DURACAO DO PERIODO') != -1:
            DGER['durper'] = int(line[21:26].strip())
        elif line.rfind('No. DE ANOS DO EST') != -1:
            DGER['nyears'] = int(line[21:26].strip())
        # elif line.rfind('MES INICIO PRE-EST') != -1:
        #     DGER['nmpre'] = int(line[21:26].strip())
        elif line.rfind('MES INICIO PRE-EST') != -1:
            DGER['mipre'] = int(line[21:26].strip())
        elif line.rfind('No. DE ANOS PRE') != -1:
            DGER['nypre'] = int(line[21:26].strip())
        elif line.rfind('No. DE ANOS POS FINAL') != -1:
            DGER['nyposf'] = int(line[21:26].strip())
        elif line.rfind('No. DE ANOS POS') != -1:
            DGER['nypos'] = int(line[21:26].strip())
        elif line.rfind('MES INICIO DO ESTUDO') != -1:
            # DGER['mi'] = int(line[21:26].strip())
            temp = re.findall(r'-?\d+\.?\d*', line)
            DGER['mi'] = int(temp[0])
            
        elif line.rfind('ANO INICIO DO ESTUDO') != -1:
            DGER['yi'] = int(line[21:26].strip())
        elif line.rfind('No DE SERIES SINT.') != -1:
            DGER['nsint'] = int(line[21:26].strip())
        elif line.rfind('ANO INICIAL HIST.') != -1:
            DGER['hiy'] = int(line[21:26].strip())
        elif line.rfind('CALCULA VOL.INICIAL') != -1:
            DGER['calcvolini'] = int(line[21:26].strip())
        elif line.rfind('TIPO SIMUL. FINAL') != -1:
            DGER['tsimfinal'] = int(line[21:26].strip())
        elif line.rfind('RACIONAMENTO PREVENT.') != -1:
            DGER['raciopreven'] = int(line[22:26].strip())
        elif line.rfind("No. ANOS MANUT.UTE'S") != -1:
            DGER['anosmanutt'] = int(line[22:26].strip())
        elif line.rfind("TENDENCIA HIDROLOGICA") != -1:
            DGER['tendhidr'] = unidecode(str(line[2:35])).strip()
            #(int(line[23:26].strip()),int(line[27:31].strip()))
        elif line.rfind('DURACAO POR PATAMAR') != -1:
            DGER['durppat'] = int(line[22:26].strip())
        elif line.rfind('OUTROS USOS DA AGUA') != -1:
            DGER['usoagua'] = int(line[22:26].strip())
        elif line.rfind('CORRECAO DESVIO') != -1:
            DGER['corredesvio'] = int(line[22:26].strip())
        elif line.rfind('AGRUPAMENTO LIVRE') != -1:
            DGER['agruplivre'] = int(line[22:26].strip())
        elif line.rfind('REPRESENT.SUBMOT.') != -1:
            DGER['repressubmot'] = int(line[22:26].strip())
        elif line.rfind('CONS. CARGA ADICIONAL') != -1:
            DGER['c_adic'] = int(line[22:26].strip())
        elif line.rfind('DESP. ANTEC.  GNL') != -1:
            DGER['despantgnl'] = int(line[22:26].strip())
        elif line.rfind('MODIF.AUTOM.ADTERM') != -1:
            DGER['modifautoadterm'] = int(line[22:26].strip())
        elif line.rfind('CONSIDERA GHMIN') != -1:
            DGER['ghmin'] = int(line[22:26].strip())
        elif line.rfind('SAR') != -1:
            try:
                DGER['sar'] = int(line[22:26].strip())
            except:
                temp = re.findall(r'-?\d+\.?\d*', line)
                DGER['sar'] = int(temp[0])
            
        elif line.rfind('CVAR') != -1:
            try:
                DGER['cvar'] = int(line[22:26].strip())
            except:
                temp = re.findall(r'-?\d+\.?\d*', line)
                DGER['cvar'] = int(temp[0])
            
        elif line.rfind('TAXA DE DESCONTO') != -1:
            try:
                DGER['txdesc'] = float(line[20:26].strip())
            except:
                DGER['txdesc'] = float(line[:10].strip())
                

    DGER['ni'] = (12 - int(DGER['mi'])+1) + (int(DGER['nyears']) - 1) * 12
    anosplan = list()
    ano_ini = DGER['yi']
    for anos in range(DGER['nyears']):
        anosplan.append(ano_ini+anos)
    DGER['yph'] = anosplan
    fobj.close()
    return DGER
