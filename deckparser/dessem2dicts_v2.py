from deckparser.importers.dessem.source import case_desc, dessem_source
from deckparser.importers.dessem.out.result_loader import ResultLoader
from deckparser.importers.dessem.loader import Loader
from collections import defaultdict
from datetime import date
import traceback
import logging

def dessem2dicts(fn, dia=None, rd=None, file_filter=None, interval_list=None, file_encoding=None, load_results=False, deck_version=2, pmo_date=None):
    return load_dessem(fn, dia, rd, file_filter, interval_list, 'dict', file_encoding, load_results, deck_version, pmo_date)

def load_dessem(fn, dia=None, rd=None, file_filter=None, interval_list=None, output_format=None, file_encoding=None, load_results=False, deck_version=2, pmo_date=None):
    dz = dessem_source(fn)
    if not dz.valid_source():
        return None
    
    available_dates = dz.available_dates()
    rd = casesRede(rd)
    dia = casesDia(dia, available_dates)
    dd = defaultdict(dict)
    for _d in dia:
        if isinstance(_d, int):
            d = dz.get_date(_d)
            if not d:
                getLogger().warning('Day not indexed: %s', str(_d))
                continue
        else: d = _d
        
        for r in rd:
            if r not in [True,False]:
                getLogger().warning('Invalid grid option (use bool True/False): %s', str(r))
            elif d in available_dates and r in dz.available_grid_options(d):
                try:
                    if load_results:
                        dt = load_dessem_result(dz, d, r, file_filter, file_encoding, output_format)
                    else:
                        dt = load_dessem_case(dz, d, r, file_filter, interval_list, file_encoding, output_format, deck_version)
                except Exception as exc:
                    print(traceback.format_exc())
                    print(exc)
                    if load_results:
                        getLogger().error('Failed to load results for case: %s', case_desc(d,r))
                    else:
                        getLogger().error('Failed to load case data: %s', case_desc(d,r))
                    continue
                if dt:
                    dd[d][r] = dt
            else:
                if isinstance(d, date):
                    getLogger().warning('Case not indexed: %s', case_desc(d,r))
                else:
                    getLogger().warning('Invalid date object (use datetime.date): %s', str(d))
    return dd

def load_dessem_case(dz, d, r, file_filter=None, interval_list=None, enc=None, fmt=None, deck_version=2):
    getLogger().info('Loading case for date %s', case_desc(d,r))
    try:
        dr = dz.make_available(d, r, result_flag=False)
    except:
        getLogger().warning('Could not open case: %s', case_desc(d,r))
        return None
    ld = Loader(dr, enc, deck_version=deck_version)
    ld.setFileFilter(file_filter)
    ld.loadAll(interval_list)
    if not fmt:
        return ld
    else:
        return ld.getData(fmt)

def load_dessem_result(dz, d, r, file_filter=None, enc=None, fmt=None):
    getLogger().info('Loading results for date %s', case_desc(d,r))
    ld = ResultLoader(None, enc)
    ld.setFileFilter(file_filter)
    try:
        dr = dz.make_available(d, r, 
                               result_flag=True, 
                               file_list=ld.getFileList())
    except:
        getLogger().warning('Could not open results: %s', case_desc(d,r))
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

def getLogger():
    return logging.getLogger(__name__)
