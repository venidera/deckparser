from numpy import int32,dtype,fromfile
from datetime import date
from os import remove

def importVAZOES(fn,hcount,dger):
    lsttipovaz = [('Vazao', int32)]
    vaztipo = dtype(lsttipovaz)
    vazdata = fromfile(fn,dtype=vaztipo,sep="")
    VAZcount = len(vazdata)
    VAZOES = dict()
    vazl = dict()
    # Inicializa dict() de vazoes para cada posto
    anocorrente = date.today().year
    for x in range(1,hcount+1):
        VAZOES[x] = dict()
        vazl[x] = list()
        for i in range(dger['hiy'],int(dger['yi'])+1):
            VAZOES[x][i] = dict()
    ano = dger['hiy']
    mes = 1
    # separar os dados de vazdata em uma lista
    vazdatalist = [ vaz[0] for vaz in vazdata ]
    totele = len(vazdatalist)
    idxele = 0
    while idxele < totele:
        posto = 1
        while posto <= hcount:
            VAZOES[posto][ano][mes] = float(vazdatalist[idxele])
            vazl[posto].append(float(vazdatalist[idxele]))
            posto = posto + 1
            idxele = idxele + 1
        if mes < 12:
            mes = mes + 1
        else:
            mes = 1
            ano = ano + 1  
    remove(fn)
    return VAZOES, VAZcount, vazl
