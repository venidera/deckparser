from deckparser.importers.imputils import searchInList, getUpdateIndexes
from logging import info,debug

def importDADGER(data, reg):
    NumPatamares = 3
    DADGER = {
        'UH': [], 'CT': [], 'UE': [], 'DP': [], 'PQ': [], 'IT': [], 'IA': [],
        'MP': [], 'VE': [], 'VM': [], 'DF': [], 'TI': [], 'MT': [], 'VI': [],
        'RE': dict(), 'AC': []
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
            if id == "UH":
                DADGER["UH"].append(importUH(line))
            elif id == "CT":
                DADGER["CT"].append(importCT(line))
            elif id == "UE":
                DADGER["UE"].append(importUE(line))
            elif id == "DP":
                DADGER["DP"].append(importDP(line))
            elif id == "PQ":
                DADGER["PQ"].append(importPQ(line))
            elif id == "IT":
                DADGER["IT"].append(importIT(line,NumPatamares))
            elif id == "IA":
                DADGER["IA"].append(importIA(line,NumPatamares))
            elif id == "TX":
                DADGER["TX"] = importTX(line)
            elif id == "DT":
                DADGER["DT"] = importDT(line)
            elif id == "MP" or id == "VE" or id == "VM" or id == "DF" or id == "TI":
                DADGER[id].append(importMPVEVMDFTI(id, line))
            elif id == "MT":
                DADGER["MT"].append(importMT(line))
            elif id == "VI":
                DADGER["VI"].append(importVI(line))
            elif id == "RE":
                importRE(line,DADGER["RE"])
            elif id == "LU":
                importLU(line,DADGER["RE"],NumPatamares)
            elif id == "FU":
                importFU(line,DADGER["RE"])
            elif id == "FT":
                importFT(line,DADGER["RE"])
            elif id == "FI":
                importFI(line,DADGER["RE"])
            elif id == "AC":
                DADGER['AC'].append(importAC(line))
        except ValueError as e:
            info(str(e)+" linha: "+str(lineNum))
            
    if reg != None:
        return DADGER[reg]
    else:
        return DADGER



   
def importUH(line):
    return {
        'CodUhe': int(line[4:7].strip()),
        'VolIni': float(line[14:24].strip())
    }

def importCT(line):
    return {
        'CodUte': int(line[4:7].strip()),
        'Estagio': int(line[24:26].strip()),
        'GtMin': [float(line[29:34].strip()),
                  float(line[49:54].strip()),
                  float(line[69:74].strip())],
        'PotEf': [float(line[34:39].strip()),
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


def importDP(line):
    DP = {
        'Estagio': int(line[4:6].strip()),
        'CodSubsistema': int(line[9:11].strip()),
        'NumPatamares': int(line[14:15].strip()),
        'Duracao': []
    }
    
    mercado = []
    
    for patamar in range(1,DP['NumPatamares']+1):
        startPos = patamar*20-1
        carga = line[startPos:startPos+10].strip()
        if carga != "":
            carga = float(carga)
            mercado.append(carga)

        DP['Duracao'].append(float(line[startPos+10:startPos+20].strip()))
        #    DuracaoTotal += Duracao[Patamar-1];

    if len(mercado)>0:
        DP['MMED'] = mercado

    return DP

def importPQ(line):
    return {
        'CodSubsistema': int(line[14:16].strip()),
        'Estagio': int(line[19:21].strip()),
        'Valor': [float(line[24:29].strip()),
                  float(line[29:34].strip()),
                  float(line[34:39].strip())]
    }

def importIT(line,numPatamares):
    IT = {
        'Estagio': int(line[4:6].strip()),
        'GerIt50': [],
        'Mande': []
    }
    for patamar in range(1,numPatamares+1):
        gerItInit = patamar*10
        mandeInit = patamar*10
        IT['GerIt50'].append(float(line[gerItInit:gerItInit+5].strip()))
        IT['Mande'].append(float(line[mandeInit:mandeInit+5].strip()))
        
    return IT
        
def importIA(line,numPatamares):
    IA = {
        'Estagio': int(line[4:6].strip()),
        'S1': line[9:11].strip(),
        'S2': line[14:16].strip(),
        'Valores': []
    }

    for patamar in range(1,numPatamares+1):
        imedInit = patamar*20-1
        IA['Valores'].append({
            'S1S2': int(line[imedInit:imedInit+10].strip()),
            'S2S1': int(line[imedInit+10:imedInit+20].strip())
        })
        
    return IA

def importTX(line):
    return float(line[4:9].strip())

def importDT(line):
    return {
        "Ano": int(line[14:18].strip()),
        "Mes": int(line[9:11].strip()),
        "Dia": int(line[4:6].strip())
    }

def importMPVEVMDFTI(id,line):
    Reg = {
        "CodUhe": int(line[4:7].strip()),
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

    return Reg

def importMT(line):
    MT = {
	"CodUte": int(line[4:7].strip()),
        "Valores": []
    }

    i = 0
    while True:
        Valor = line[14+i*5:14+i*5+5].strip()
        if i == 17 or Valor == "":
            break
        MT["Valores"].append(float(Valor))
        i+=1
    return MT
            
def importVI(line):
    VI = {
        "CodUhe": int(line[4:7].strip()),
        "Duracao": int(line[9:12].strip()),
        "VazDef": []
    }

    for i in range(0,5):
        VI["VazDef"].append(float(line[14+i*5:14+i*5+5].strip()))
    return VI

def importRE(line,RE):
    id = int(line[4:7].strip())
    RE[id] = {
        "EstagioIni": int(line[9:11].strip()),
        "EstagioFim": int(line[14:16].strip()),
        "LU": [],
        "FU": [],
        "FT": [],
        "FI": [],
        "FE": []
    }

def importLU(line,RE,numPatamares):
    id = int(line[4:7].strip())

    LU = {
        "Estagio": int(line[9:11].strip()),
        "Valores": []
    }

    for patamar in range(1,numPatamares+1):
        init = 14+(patamar-1)*20
        inferior =  line[init:init+10].strip()
        limite = {}
        if inferior != "":
            limite["Inferior"] = float(inferior)

        init = 24+(patamar-1)*20
        superior = line[init:init+10].strip()
        if superior != "":
            limite["Superior"] = float(superior)

        LU["Valores"].append(limite)
        
    RE[id]["LU"].append(LU)

def importFU(line, RE):
    id = int(line[4:7].strip())
    RE[id]["FU"].append({
        "Estagio": int(line[9:11].strip()),
        "CodUhe": int(line[14:17].strip()),
        "Valor": float(line[19:29].strip())
    })

def importFT(line, RE):
    id = int(line[4:7].strip())
    RE[id]["FT"].append({
        "Estagio": int(line[9:11].strip()),
        "CodUte": int(line[14:17].strip()),
        "Valor": float(line[24:34].strip())
    })

def importFI(line, RE):
    id = int(line[4:7].strip())
    RE[id]["FI"].append({
        "Estagio": int(line[9:11].strip()),
        "SSOrigem": line[14:16].strip(),
        "SSDestino": line[19:21].strip(),
        "Valor": float(line[24:34].strip())
    })

def importAC(line):
    AC = {
        "CodUhe": int(line[4:7].strip()),
        "Mnemonico": line[9:15].strip(),
        "Mes": line[69:72].strip()
    }

    estagio = line[74:75].strip()
    if estagio != "":
        AC["Estagio"] = int(estagio)


    if AC["Mnemonico"] == "NOMEUH":
        AC["Valor"] = line[19:31].strip()
    if AC["Mnemonico"] == "NUMPOS" or AC["Mnemonico"] == "NUMJUS" or \
       AC["Mnemonico"] == "NUMCON" or AC["Mnemonico"] == "VERTJU" or \
       AC["Mnemonico"] == "VAZMIN" or AC["Mnemonico"] == "NUMBAS" or \
       AC["Mnemonico"] == "TIPTUR" or AC["Mnemonico"] == "TIPERH" or \
       AC["Mnemonico"] == "JUSENA":
        AC["Valor"] = int(line[19:24].strip())
    elif AC["Mnemonico"] == "DESVIO" or AC["Mnemonico"] == "POTEFE" or \
         AC["Mnemonico"] == "ALTEFE" or AC["Mnemonico"] == "NCHAVE":
        AC["Indice"] = int(line[19:24].strip())
        AC["Valor"] = float(line[24:34].strip())
    elif AC["Mnemonico"] == "VOLMIN" or AC["Mnemonico"] == "VOLMAX" or \
         AC["Mnemonico"] == "PROESP" or AC["Mnemonico"] == "PERHID" or \
         AC["Mnemonico"] == "JUSMED":
        AC["Valor"] = float(line[19:29].strip())
    elif AC["Mnemonico"] == "COTVOL" or AC["Mnemonico"] == "COTARE":
        AC["Indice"] = int(line[19:24].strip())
        AC["Valor"] = float(line[24:39].strip())
    elif AC["Mnemonico"] == "COFEVA" or AC["Mnemonico"] == "NUMMAQ" or \
         AC["Mnemonico"] == "VAZEFE":
        AC["Indice"] = int(line[19:24].strip())
        AC["Valor"] = int(line[24:29].strip())

    return AC
