'''
Created on 2 de nov de 2018

@author: Renan Maciel
'''
from deckparser.importers.dessem.loader import Loader
from deckparser.importers.dessem.out.result_loader import ResultLoader
from deckparser.dessemsource import dessem_source
from datetime import date
import logging

def dessem2dicts(fn, dia=None, rd=None, file_filter=None, interval_list=None, file_encoding=None, load_results=False):
    return load_dessem(fn, dia, rd, file_filter, interval_list, 'dict', file_encoding, load_results)

def getLogger():
    return logging.getLogger(__name__)

def load_dessem(fn, dia=None, rd=None, file_filter=None, interval_list=None, output_format=None, file_encoding=None, load_results=False, deck_version=1):
    dz = dessem_source(fn, load_results)
    if dz.validSource():
        rd = casesRede(rd)
        dia = casesDia(dia, dz.dias.keys())
        dd = {}
        for _d in dia:
            if isinstance(_d, int):
                d = dz.getDate(_d)
                if not d:
                    getLogger().warning('Day not indexed: %s', str(_d))
                    continue
            else: d = _d
            
            for r in rd:
                if r not in [True,False]:
                    getLogger().warning('Invalid grid option (use bool True/False): %s', str(r))
                elif d in dz.dias and r in dz.dias[d]:
                    if d not in dd: dd[d] = {}
                    if load_results:
                        dt = load_dessem_result(dz, d, r, file_filter, file_encoding, output_format)
                    else:
                        dt = load_dessem_case(dz, d, r, file_filter, interval_list, file_encoding, output_format, deck_version)
                    if dt:
                        dd[d][r] = dt
                else:
                    if isinstance(d, date):
                        getLogger().warning('Case not indexed: %s %s', str(d), optGridToStr(r))
                    else:
                        getLogger().warning('Invalid date object (use datetime.date): %s', str(d))
        return dd
    else:
        return None

def optGridToStr(r):
    return ('Com Rede' if r else 'Sem Rede')

def load_dessem_case(dz, d, r, file_filter=None, interval_list=None, enc=None, fmt=None, deck_version=1):
    rd = optGridToStr(r)
    getLogger().info('Loading case for date %s %s', str(d), str(rd))
    try:
        dr = dz.extractAllFiles(d, r)
    except:
        getLogger().warning('Could not open case: %s %s', str(d), str(r))
        return None
    ld = Loader(dr, enc, deck_version=deck_version)
    ld.setFileFilter(file_filter)
    ld.loadAll(interval_list)
    if not fmt:
        return ld
    else:
        return ld.getData(fmt)

def load_dessem_result(dz, d, r, file_filter=None, enc=None, fmt=None):
    rd = optGridToStr(r)
    getLogger().info('Loading results for date %s %s', str(d), str(rd))
    ld = ResultLoader(None, enc)
    ld.setFileFilter(file_filter)
    try:
        dr = dz.extractFiles(d, r, ld.getFileList())
    except:
        getLogger().warning('Could not open results: %s %s', str(d), str(r))
        return None
    ld.setDirDS(dr)
    ld.loadAll()
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
