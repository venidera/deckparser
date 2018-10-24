from numpy import dtype, fromfile, int32, float32

def importVAZOES(fn,blockSize):
    vazoes = dict()
    vazaoDef = [('dado',int32)]
    vazaoDtype = dtype(vazaoDef)
    
    vazaoData = fromfile(fn, dtype=vazaoDtype, sep="")

    # registro 1 - número de postos, número de estágios e aberturas de cada estágio
    vazoes["numPostos"] = vazaoData[0]['dado']
    vazoes["numEstagios"] = vazaoData[1]['dado']
    vazoes["aberturas"] = []

    # número de aberturas do último estágio
    for i in range(vazoes["numEstagios"]):
        if vazaoData[2+i]['dado'] != 1 and i != vazoes["numEstagios"]-1:
            raise RuntimeError("Número de aberturas diferente de 1 do estágio "+str(i+1))
        vazoes["aberturas"].append(vazaoData[2+i]['dado'])
        

    # registro 2 - codigo das usinas consideradas
    vazoes["codUhe"] = []
    for i in range(vazoes["numPostos"]):
        vazoes["codUhe"].append(vazaoData[blockSize+i]['dado'])


    # registro 3 - número de semanas completas do estudo, nro de dias excluídos do estagio \
    # seguinte ao mes inicial,

    vazoes["semanasCompletas"] = vazaoData[blockSize*2]['dado']
    vazoes["numDiasExcl"] = vazaoData[blockSize*2+1]['dado']
    vazoes["mesIni"] = vazaoData[blockSize*2+2]['dado']
    vazoes["anoIni"] = vazaoData[blockSize*2+3]['dado']

    # registro 4 - probabilidades (pula)

    # registro 5 - vazoes 
    skip = int(vazoes["aberturas"][vazoes["numEstagios"]-1]/blockSize+1)*blockSize + 3*blockSize;

    vazoes["prevSem"] = []
    pos = 0
    for estagio in range(1,vazoes["semanasCompletas"]+1):
        vazoes["prevSem"].append([])
        for posto in range(1,blockSize+1):
            vazoes["prevSem"][estagio-1].append(vazaoData[skip+pos]['dado'])
            pos += 1

    return vazoes
