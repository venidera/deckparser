from logging import info,debug

def importDADGNL(data, reg=None):
    numPatamares = 3
    DADGNL = {
        'TG': dict(), 'GS': dict(),  'NL': dict(), 'GL': dict()
    }

    lineNum = 0
    for line in data:
        lineNum += 1
        if line[0]=='&':
            continue

        id = line[0:2].strip()

        if reg != None and id != reg:
            continue

        try:
            if id == 'TG':
                importTG(line,DADGNL['TG'])
            elif id == 'GS':
                importGS(line,DADGNL['GS'])
            elif id == 'NL':
                importNL(line,DADGNL['NL'])
            elif id == 'GL':
                importGL(line,DADGNL['GL'])
        except ValueError as e:
            info(str(e) + " linha: " + str(lineNum))

    if reg != None:
        return DADGNL[reg]
    else:
        return DADGNL

def importTG(line,TG):
    codUte = int(line[4:7].strip())
    estagio = int(line[24:26].strip())

    if codUte not in TG:
        TG[codUte] = dict()

    TG[codUte][estagio] = {
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

def importGS(line,GS):
    iMes = int(line[4:6].strip())
    semanas = int(line[9])

    GS[iMes] = semanas

def importNL(line,NL):
    codUte = int(line[4:7].strip())
    lag = int(line[14])
    NL[codUte] = lag

def importGL(line,GL):
    codUte = int(line[4:7].strip())
    estagio = int(line[14:16].strip())

    if codUte not in GL:
        GL[codUte] = dict()

    GL[codUte][estagio] = {
        'Geracao': [float(line[19:29].strip()),
                    float(line[34:44].strip()),
                    float(line[49:59].strip())],
        'Duracao': [float(line[29:34].strip()),
                    float(line[44:49].strip()),
                    float(line[59:64].strip())],
        'Inicio': {
            'Dia': int(line[65:67].strip()),
            'Mes': int(line[67:69].strip()),
            'Ano': int(line[69:73].strip())
        }
    }
