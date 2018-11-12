'''
Created on 2 de nov de 2018

@author: Renan Maciel
'''
from deckparser.importers.dessem.loader import Loader
from deckparser.dessemzipped import DessemZipped
from datetime import date
import logging

def dessem2dicts(fn, dia=None, rd=None, opt={'filename_pattern':1}):
    opt['output_format'] = 'dict'
    return load_dessem(fn, dia, rd, opt)

def getLogger():
    return logging.getLogger(__name__)

def load_dessem(fn, dia=None, rd=None, opt={'filename_pattern':1, 'output_format':'dict'}):
    """
    Open the zipped file and start to import data
    """
    dz = DessemZipped(fn, opt.get('filename_pattern'))
    if dz.zipLoaded():
        rd = casesRede(rd)
        dia = casesDia(dia, dz.dias.keys())
        dd = {}
        for d in dia:
            for r in rd:
                if r not in [True,False]:
                    getLogger().warning('Invalid grid option (use bool True/False): %s', str(r))
                elif d in dz.dias and r in dz.dias[d]:
                    if d not in dd: dd[d] = {}
                    try:
                        dt = load_dessem_case(dz, d, r, opt)
                    except:
                        getLogger().warning('Retrying loading case: %s %s', str(d), optGridToStr(r))
                        optAlt = {}
                        for ko in opt: optAlt[ko] = opt[ko]
                        optAlt['file_encoding'] = 'latin_1'
                        dt = load_dessem_case(dz, d, r, optAlt)
                    if dt:
                        dd[d][r] = dt
                else:
                    if isinstance(d, date):
                        getLogger().warning('Date not indexed: %s', str(d))
                    else:
                        getLogger().warning('Invalid date object (use datetime.date): %s', str(d))
        return dd
    else:
        return None

def optGridToStr(r):
    return ('Com Rede' if r else 'Sem Rede')

def load_dessem_case(dz, d, r, opt):
    rd = optGridToStr(r)
    print('Loading case for date {:s} {:s}'.format(str(d), str(rd)))
    getLogger().info('Loading case for date %s %s', str(d), str(rd))
    try:
        dr = dz.extractAllFiles(d, r)
    except:
        getLogger().warning('Could not open case: %s %s', str(d), str(r))
        return None
    ld = Loader(dr, opt.get('file_encoding'))
    ld.loadAll()
    fmt = opt.get('output_format')
    if not fmt:
        return ld
    else:
        return ld.getData(fmt)

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
