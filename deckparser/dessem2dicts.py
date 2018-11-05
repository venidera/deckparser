'''
Created on 2 de nov de 2018

@author: Renan Maciel
'''
from deckparser.importers.dessem.loader import Loader
from deckparser.dessemzipped import DessemZipped
from datetime import date

def dessem2dicts(fn, dia = None, rd = None):
    """
    Open the zipped file and start to import data into python dicts and lists
    """
    dz = DessemZipped(fn=fn)
    if dz.zipLoaded():
        rd = casesRede(rd)
        dia = casesDia(dia, dz.dias.keys())
        dd = {}
        for d in dia:
            for r in rd:
                if r not in [True,False]:
                    raise ValueError("Opcao de rede invalida (use bool True/False): "+str(r))
                if d in dz.dias and r in dz.dias[d]:
                    if d not in dd: dd[d] = {}
                    print('-'*50+'\nCarregando dia '+str(d)+' '+('Com Rede' if r else 'Sem Rede')+'\n'+'-'*50)
                    dr = dz.extractAllFiles(d, r)
                    ld = Loader(dr)
                    ld.loadAll()
                    dd[d][r] = ld.toDict()
                else:
                    if isinstance(d, date):
                        raise ValueError("Dia nao indexado: "+str(d))
                    else:
                        raise ValueError("Dia invalido (use objeto datetime.date): "+str(d))
        return dd
    else:
        return None

def casesRede(rd):
    if rd is None:
        return [True,False]
    if isinstance(rd, list):
        return rd
    return [rd]
    
def casesDia(dia, df):
    if dia is None:
        return df
    if isinstance(dia, list):
        return dia
    return [dia]
