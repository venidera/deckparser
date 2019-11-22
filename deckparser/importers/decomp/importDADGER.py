from logging import info,debug

def importDADGER(data, reg=None):
    numPatamares = 3
    DADGER = {
        'UH': dict(), 'CT': dict(), 'UE': [], 'DP': dict(), 'PQ': dict(),
        'IT': dict(), 'IA': dict(), 'MP': dict(), 'VE': dict(), 'VM': dict(),
        'DF': dict(), 'TI': dict(), 'MT': dict(), 'VI': dict(), 'RE': dict(),
        'AC': dict(), 'TE': '', 'HQ': dict(), 'HV': dict()
    }

    lineNum = 0
    for line in data:
        lineNum += 1
        if line[0]=='&':
            continue

        id = line[0:2].strip()

        if reg != None and id != reg and \
           (reg == "RE" and id != "LU" and \
            id != "FU" and id != 'FT' and id!='FI'):
            continue
       
        try:
            if id == "TE":
                DADGER["TE"] = line[4:84].strip()
            elif id == "UH":
                importUH(line,DADGER["UH"])
            elif id == "CT":
                importCT(line,DADGER["CT"])
            elif id == "UE":
                DADGER["UE"].append(importUE(line))
            elif id == "DP":
                importDP(line,DADGER["DP"])
            elif id == "PQ":
                importPQ(line,DADGER["PQ"])
            elif id == "IT":
                importIT(line,numPatamares,DADGER["IT"])
            elif id == "IA":
                importIA(line,numPatamares,DADGER["IA"])
            elif id == "TX":
                DADGER["TX"] = importTX(line)
            elif id == "DT":
                DADGER["DT"] = importDT(line)
            elif id == "MP" or id == "VE" or id == "VM" or id == "DF" or id == "TI":
                importMPVEVMDFTI(line, id, DADGER[id])
            elif id == "MT":
                importMT(line, DADGER["MT"])
            elif id == "VI":
                importVI(line,DADGER["VI"])
            elif id == "RE":
                importRE(line,DADGER["RE"])
            elif id == "LU":
                importLU(line,DADGER["RE"],numPatamares)
            elif id == "FU":
                importFU(line,DADGER["RE"])
            elif id == "FT":
                importFT(line,DADGER["RE"])
            elif id == "FI":
                importFI(line,DADGER["RE"])
            elif id == "AC":
                importAC(line,DADGER['AC'])
            elif id == "HQ":
                importHQ(line,DADGER["HQ"])
            elif id == "LQ":
                importLQ(line,DADGER["HQ"],numPatamares)
            elif id == "CQ":
                importCQ(line,DADGER["HQ"])
            elif id == "HV":
                importHV(line,DADGER["HV"])
            elif id == "LV":
                importLV(line,DADGER["HV"])
            elif id == "CV":
                importCV(line,DADGER["HV"])
        except ValueError as e:
            info(str(e)+" linha: "+str(lineNum))
            
    if reg != None:
        return DADGER[reg]
    else:
        return DADGER



   
def importUH(line, UH):
    UH[int(line[4:7].strip())] = {
        'VolIni': float(line[14:24].strip())
    }

def importCT(line, CT):
    codUte = int(line[4:7].strip())
    estagio = int(line[24:26].strip())

    if codUte not in CT:
        CT[codUte] = dict()

    CT[codUte][estagio] = {
        'GtMin': [float(line[29:34].strip()),
                  float(line[49:54].strip()),
                  float(line[69:74].strip())],
        'PotEfe': [float(line[34:39].strip()),
                  float(line[54:59].strip()),
                  float(line[74:79].strip())],
        'Custo': [float(line[39:49].strip()),
                  float(line[59:69].strip()),
                  float(line[79:89].strip())],
    }


def importUE(line):
    return {
        'Nome': line[14:26].strip(),
        'Jusante': int(line[29:32].strip()),
        'Montante': int(line[34:37].strip()),
        'VazMin': float(line[39:49].strip()),
        'VazMax': float(line[49:59].strip()),
        'Consumo': float(line[59:69].strip())
    }


def importDP(line, DP):
    estagio = int(line[4:6].strip())
    codSubsistema = int(line[9:11].strip())
    
    if estagio not in DP:
        DP[estagio] = dict()
    
    DP[estagio][codSubsistema] = {
        'NumPatamares': int(line[14:15].strip()),
        'Duracao': []
    }

    mercado = []
    for patamar in range(1,DP[estagio][codSubsistema]['NumPatamares']+1):
        startPos = patamar*20-1
        carga = line[startPos:startPos+10].strip()
        if carga != "":
            carga = float(carga)
            mercado.append(carga)

        DP[estagio][codSubsistema]['Duracao'].append(float(line[startPos+10:startPos+20].strip()))

    if len(mercado)>0:
        DP[estagio][codSubsistema]['MMED'] = mercado

def importPQ(line, PQ):
    estagio = int(line[19:21].strip())
    codSubsistema = int(line[14:16].strip())
    
    if estagio not in PQ:
        PQ[estagio] = dict()

    if codSubsistema not in PQ[estagio]:        
        PQ[estagio][codSubsistema] = list()
        
    PQ[estagio][codSubsistema].append({
        'Nome': line[4:14].strip(),
        'Valor': [float(line[24:29].strip()),
                  float(line[29:34].strip()),
                  float(line[34:39].strip())]
    })

def importIT(line,numPatamares,IT):
    estagio = int(line[4:6].strip())
    IT[estagio] = {
        'GerIt50': [],
        'Mande': []
    }
    for patamar in range(1,numPatamares+1):
        gerItInit = 10+patamar*10
        mandeInit = 15+patamar*10
        IT[estagio]['GerIt50'].append(float(line[gerItInit:gerItInit+5].strip()))
        IT[estagio]['Mande'].append(float(line[mandeInit:mandeInit+5].strip()))
        
        
def importIA(line,numPatamares,IA):
    estagio = int(line[4:6].strip())
    if estagio not in IA:
        IA[estagio] = dict()
    s1 = line[9:11].strip()
    s2 = line[14:16].strip()

    if s1 not in IA[estagio]:
        IA[estagio][s1] = dict()

    if s2 not in IA[estagio]:
        IA[estagio][s2] = dict()

    IA[estagio][s1][s2] = list()
    IA[estagio][s2][s1] = list()
        
    for patamar in range(1,numPatamares+1):
        imedInit = patamar*20-1
        IA[estagio][s1][s2].append(int(line[imedInit:imedInit+10].strip()))
        IA[estagio][s2][s1].append(int(line[imedInit+10:imedInit+20].strip()))
        
    return IA

def importTX(line):
    return float(line[4:9].strip())

def importDT(line):
    return {
        "Ano": int(line[14:18].strip()),
        "Mes": int(line[9:11].strip()),
        "Dia": int(line[4:6].strip())
    }

def importMPVEVMDFTI(line,id,obj):
    codUhe = int(line[4:7].strip())
    Reg = {
        "Unidade": "m3/s",
        "Valores": []
    }

    if id == "VE":
        Reg["Unidade"] = "%"
    elif id =="MP":
        Reg["Unidade"] = ""
       
    i = 0;
    while True:
        Valor = line[9+i*5:9+i*5+5].strip()
        if i == 17 or Valor == "":
            break
        Reg["Valores"].append(float(Valor))
        i += 1

    obj[codUhe] = Reg

def importMT(line,MT):
    codUte = int(line[4:7].strip())
    valores = []

    i = 0
    while True:
        valor = line[14+i*5:14+i*5+5].strip()
        if i == 17 or valor == "":
            break
        valores.append(float(valor))
        i+=1
    MT[codUte] = valores
            
def importVI(line,VI):
    codUhe = int(line[4:7].strip())
    VI[codUhe] = {
        "Duracao": int(line[9:12].strip()),
        "VazDef": []
    }

    for i in range(0,5):
        VI[codUhe]["VazDef"].append(float(line[14+i*5:14+i*5+5].strip()))

def importRE(line,RE):
    id = int(line[4:8].strip())
    RE[id] = {
        "EstagioIni": int(line[9:11].strip()),
        "EstagioFim": int(line[14:16].strip()),
        "LU": dict(),
        "FU": [],
        "FT": [],
        "FI": [],
        "FE": []
    }

def importLU(line,RE,numPatamares):
    id = int(line[4:8].strip())

    estagio = int(line[9:11].strip())
    LU = list()

    for patamar in range(numPatamares):
        init = 14+patamar*20
        inferior =  line[init:init+10].strip()
        limite = {}
        if inferior != "":
            limite["Inferior"] = float(inferior)

        init = 24+patamar*20
        superior = line[init:init+10].strip()
        if superior != "":
            limite["Superior"] = float(superior)

        LU.append(limite)
        
    RE[id]["LU"][estagio] = LU

def importFU(line, RE):
    id = int(line[4:8].strip())
    RE[id]["FU"].append({
        "Estagio": int(line[9:11].strip()),
        "CodUhe": int(line[14:17].strip()),
        "Valor": float(line[19:29].strip())
    })

def importFT(line, RE):
    id = int(line[4:8].strip())
    RE[id]["FT"].append({
        "Estagio": int(line[9:11].strip()),
        "CodUte": int(line[14:17].strip()),
        "Valor": float(line[24:34].strip())
    })

def importFI(line, RE):
    id = int(line[4:8].strip())
    RE[id]["FI"].append({
        "Estagio": int(line[9:11].strip()),
        "SSOrigem": line[14:16].strip(),
        "SSDestino": line[19:21].strip(),
        "Valor": float(line[24:34].strip())
    })

def importAC(line, AC):
    codUhe = int(line[4:7].strip())
    reg = {
        "Mnemonico": line[9:15].strip(),
        "Mes": line[69:72].strip()
    }

    try:
        reg["Estagio"] = int(line[74:75].strip())
    except Exception as e:
        pass
    
    try:
        reg["Ano"] = int(line[76:80].strip())
    except Exception as e:
        pass


    if reg["Mnemonico"] == "NOMEUH":
        reg["Valor"] = line[19:31].strip()
    if reg["Mnemonico"] == "NUMPOS" or reg["Mnemonico"] == "NUMJUS" or \
       reg["Mnemonico"] == "NUMCON" or reg["Mnemonico"] == "VERTJU" or \
       reg["Mnemonico"] == "VAZMIN" or reg["Mnemonico"] == "NUMBAS" or \
       reg["Mnemonico"] == "TIPTUR" or reg["Mnemonico"] == "TIPERH" or \
       reg["Mnemonico"] == "JUSENA":
        reg["Valor"] = int(line[19:24].strip())
    elif reg["Mnemonico"] == "DESVIO" or reg["Mnemonico"] == "POTEFE" or \
         reg["Mnemonico"] == "ALTEFE" or reg["Mnemonico"] == "NCHAVE":
        reg["Indice"] = int(line[19:24].strip())
        reg["Valor"] = float(line[24:34].strip())
    elif reg["Mnemonico"] == "VOLMIN" or reg["Mnemonico"] == "VOLMAX" or \
         reg["Mnemonico"] == "PROESP" or reg["Mnemonico"] == "PERHID" or \
         reg["Mnemonico"] == "JUSMED":
        reg["Valor"] = float(line[19:29].strip())
    elif reg["Mnemonico"] == "COTVOL" or reg["Mnemonico"] == "COTARE":
        reg["Indice"] = int(line[19:24].strip())
        reg["Valor"] = float(line[24:39].strip())
    elif reg["Mnemonico"] == "COTVAZ":
        reg["Numero"] = int(line[19:24].strip())
        reg["Indice"] = int(line[24:29].strip())
        reg["Valor"] = float(line[29:44].strip())        
    elif reg["Mnemonico"] == "COFEVA" or reg["Mnemonico"] == "NUMMAQ" or \
         reg["Mnemonico"] == "VAZEFE":
        reg["Indice"] = int(line[19:24].strip())
        reg["Valor"] = int(line[24:29].strip())

    if codUhe not in AC:
        AC[codUhe] = []
    AC[codUhe].append(reg)


def importHQ(line,HQ):
    id = int(line[4:7].strip())
    HQ[id] = {
        "EstagioIni": int(line[9:11].strip()),
        "EstagioFim": int(line[14:16].strip()),
        "LQ": dict(),
        "CQ": dict()
    }

def importLQ(line,HQ,numPatamares):
    id = int(line[4:7].strip())
    estagio = int(line[9:11].strip())
    LQ = list()

    for patamar in range(numPatamares):
        init = 14+patamar*20
        inferior =  line[init:init+10].strip()
        limite = {}
        if inferior != "":
            limite["Inferior"] = float(inferior)

        init = 24+patamar*20
        superior = line[init:init+10].strip()
        if superior != "":
            limite["Superior"] = float(superior)

        LQ.append(limite)
        
    HQ[id]["LQ"][estagio] = LQ
    
    
def importCQ(line,HQ):
    id = int(line[4:7].strip())
    estagio = int(line[9:11].strip())
    HQ[id]['CQ'][estagio] = {
        'codUhe': int(line[14:17].strip()),
        'coef': float(line[19:29].strip()),
        'tipo': line[34:38].strip()
    }
    
def importHV(line,HV):
    id = int(line[4:7].strip())
    HV[id] = {
        "EstagioIni": int(line[9:11].strip()),
        "EstagioFim": int(line[14:16].strip()),
        "LV": dict(),
        "CV": dict()
    }

def importLV(line,HV):
    id = int(line[4:7].strip())
    estagio = int(line[9:11].strip())

    inferior =  line[14:24].strip()
    limite = {}
    if inferior != "":
        limite["Inferior"] = float(inferior)

    superior = line[24:34].strip()
    if superior != "":
        limite["Superior"] = float(superior)

    HV[id]["LV"][estagio] = limite
    
    
def importCV(line,HV):
    id = int(line[4:7].strip())
    estagio = int(line[9:11].strip())

    if estagio not in HV[id]['CV']:
        HV[id]['CV'][estagio] = list()
    HV[id]['CV'][estagio].append({
        'codUhe': int(line[14:17].strip()),
        'coef': float(line[19:29].strip()),
        'tipo': line[34:38].strip()
    })
