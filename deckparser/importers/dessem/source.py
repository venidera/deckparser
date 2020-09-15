from deckparser.importers.dessem.util.pmo import real_date
from deckparser.importers.dessem.out.result_loader import ResultLoader
from deckparser.importers.dessem.loader import Loader
from difflib import SequenceMatcher
from collections import defaultdict
from datetime import date
import logging
import zipfile
import os
import re
import shutil

def dessem_source(fn, options=None):
    options = options or {}
    options.setdefault('source_rank', {
        'level': 10, 
        'name': {
            'Reprocessamento': 1
            }
        })
    return DessemSource(fn, options)

def case_desc(d,r):
    return '{} {}'.format(d.strftime('%Y-%m-%d'), ('com' if r else 'sem') + ' rede')

class DessemSource:
    
    def __init__(self, source_path, options=None):
        if os.path.isdir(source_path):
            self.root_source = PmoDessemDirSource(source_path)
        elif zipfile.is_zipfile(source_path):
            self.root_source = PmoDessemZippedSource(source_path)
        else:
            raise Exception('Invalid source: '+str(source_path))
        
        self.prepare(options)
    
    def prepare(self, options):
        max_level = options.get('max_level', 5)
        self.root_source.build(max_level)
        self.deck_index = self.root_source.export(options)
        self.extracted_sources = defaultdict(dict)
        
        ed = options.get('extract_to')
        if not ed:
            ed = self.root_source.tempdir()
            try:
                os.makedirs(ed, exist_ok=True)
            except:
                # TODO usar tempdir
                raise
        self.extracted_dir = ed
    
    def __del__(self):
        self.remove_extracted_dir()
    
    def remove_extracted_dir(self):
        ed = self.extracted_dir
        getLogger().info('Removing extracted dir: {}'.format(ed))
        try:
            shutil.rmtree(self.extracted_dir)
        except:
            getLogger().warn('Failed removing extracted dir: {}'.format(ed))
    
    def type_check(self, deck, result_flag):
        if result_flag is None:
            return True
        elif result_flag:
            return deck.is_result()
        else:
            return not deck.is_result()
    
    def adapt_deck_list(self, d_list, result_flag):
        new_d_list = [d for d in d_list 
                      if self.type_check(d['deck'], result_flag)]
        
        if len(new_d_list) > 0:
            return new_d_list
        return d_list
    
    def valid_source(self):
        return len(self.deck_index) > 0
    
    def available_dates(self):
        return sorted([d for d,_ in self.deck_index.keys()])
    
    def available_grid_options(self, deck_date=None):
        return sorted([r for d,r in self.deck_index.keys()
                       if deck_date is None or d == deck_date])
    
    def print_index(self, detailed=False):
        print('Available cases:')
        for (d,r),d_list in self.deck_index.items():
            print(case_desc(d, r))
            if not detailed:
                continue
            for d in d_list:
                print('\t{} (rank: {:.4f})'.format(
                    d['deck'].complete_path(),
                    d['rank']
                    ))
    
    def listIndex(self):
        return sorted(self.deck_index.keys())
    
    def get_date(self, dia):
        for d,_ in self.deck_index.keys():
            if d.day == dia:
                return d
    
    def make_available(self, dia, r, result_flag, file_list=None):
        k = (dia,r)
        deck = self.extracted_sources.get(k,{}).get(result_flag)
        if deck:
            return deck
        
        cd = case_desc(dia,r)
        self.getLogger().info('Making deck available: {}'.format(cd))
        d_list = self.deck_index.get(k)
        if not d_list or len(d_list) == 0:
            self.getLogger().warning('Deck not available: {}'.format(cd))
            return None
        
        d_list = self.adapt_deck_list(d_list, result_flag)
        for d in d_list:
            deck = d['deck']
            orig_deck = deck
            if isinstance(deck, DeckDessemInnerZippedSource):
                deck = deck.make_available(self.extracted_dir)
            if isinstance(deck, DeckDessemZippedSource):
                deck = deck.make_available(self.extracted_dir, file_list)
            if isinstance(deck, DeckDessemDirSource):
                self.extracted_sources[k][result_flag] = deck
                self.getLogger().debug('Original source: {}'.format(orig_deck.complete_path()))
                self.getLogger().debug('Extracted source: {}'.format(deck.complete_path()))
                return deck.source_path
        
        self.getLogger().warning('There is no valid deck source: {}'.format(cd))
    
    def getLogger(self):
        return logging.getLogger(__name__)

class DirSource:
    
    def __init__(self, source_path):
        self.source_path = source_path
    
    def key(self):
        self.source_path
    
    def base_name(self):
        return os.path.basename(self.source_path)
    
    def file_path(self):
        return self.source_path
    
    def complete_path(self):
        return self.file_path()
    
    def list_all(self, level=0, curr_path=None):
        curr_path = curr_path or self.source_path
        items = []
        if level > 0:
            for inner_path in os.listdir(curr_path):
                p = os.path.join(curr_path, inner_path)
                if os.path.isdir(p):
                    items.extend([
                        os.path.join(inner_path, sd)
                        for sd in self.list_all(level-1, p)
                        ])
        else:
            items.extend(os.listdir(curr_path))
        return items
    
    def list_files_name(self):
        return [f for f in self.list_all()
                if os.path.isfile(os.path.join(self.source_path, f))]
    
    def to_dict(self):
        return {
            'source_path': self.source_path
            }

class ZippedSource:
    
    def __init__(self, zip_file_path, zip_dir):
        self.zip_file_path = zip_file_path
        self.z = zipfile.ZipFile(zip_file_path, 'r')
        self.zip_dir = self.__init_zip_dir(zip_dir)
    
    def key(self):
        k = self.zip_file_path
        if len(self.zip_dir):
            return k + '/' + '/'.join(self.zip_dir)
        return k
    
    def base_name(self):
        if len(self.zip_dir):
            return self.zip_dir[-1]
        dn = os.path.basename(self.zip_file_path)
        return dn.replace('.zip','')
    
    def file_path(self):
        return self.zip_file_path
    
    def complete_path(self):
        return self.key()
    
    def __init_zip_dir(self, zd):
        if zd is None:
            return []
        if isinstance(zd, list):
            return zd
        if isinstance(zd, str):
            return self.break_path(zd)
        raise TypeError('Invalid zip dir type: '+str(zd))
    
    def break_path(self, zn):
        return [s for s in zn.split('/') if len(s)]
    
    def list_all(self, level=0):
        return [info.filename
                for info in self.z.infolist()
                if self.__is_contained(info.filename, level)]
    
    def list_files_name(self):
        return [self.__adapt_zip_filename(info.filename)
                for info in self.z.infolist()
                if self.__is_subdir_file(info)]
    
    def __adapt_zip_filename(self, zn):
        name_parts = self.break_path(zn)
        return name_parts[-1]
    
    def __is_subdir_file(self, zip_info):
        return not zip_info.is_dir() and self.__is_contained(zip_info.filename)
    
    def __is_contained(self, zn, level=0):
        name_parts = self.break_path(zn)
        if len(name_parts) != len(self.zip_dir)+level+1: # dirs + subdirs + name
            return False
        for i,zd in enumerate(self.zip_dir):
            if name_parts[i] != zd:
                return False
        return True
    
    def to_dict(self):
        return {
            'zip_path': self.zip_file_path,
            'zip_dir': self.zip_dir
            }

class InnerZippedSource(ZippedSource):
    
    def base_name(self):
        return self.zip_dir[-1].replace('.zip','')
    
    def list_all(self, _level=0): return []
    def list_files_name(self): return []


class PmoDessemSource:
    
    def __init__(self):
        self.metadata = {}
        self.valid = {'filename': self.capture_pmo_metadata()}
    
    def pmo_key(self):
        d = self.metadata
        return date(d['ano'], d['mes'], 1)
    
    def list_source_contents(self): raise NotImplementedError()
    def new_deck_source(self, _inner_path): raise NotImplementedError()
    def new_pmo_source(self, _inner_path): raise NotImplementedError()
    
    def is_empty(self):
        return len(self.contained_decks) + len(self.contained_sources) == 0
    
    def build(self, max_level=1):
        self.contained_decks = list()
        self.contained_sources = list()
        if max_level < 1:
            return
        
        path_list = self.list_source_contents()
        for inner_path in path_list:
            ds = self.new_deck_source(inner_path)
            if ds:
                self.contained_decks.append(ds)
            
            ps = self.new_pmo_source(inner_path)
            if ps:
                ps.build(max_level-1)
                if not ps.is_empty():
                    self.contained_sources.append(ps)
    
    def export(self, options=None):
        options = options or {}
        sr = options.get('source_rank')
        as_dict = options.get('as_dict')
        
        if sr:
            return self.deck_by_case(
                as_dict = as_dict,
                source_index = self.rank_sources(sr)
                )
        return self.deck_by_case(as_dict = as_dict)
    
    def deck_by_case(self, as_dict=False, source_index=None):
        deck_index = defaultdict(list)
        for d in self.contained_decks:
            deck_index[d.case_key()].append({'deck': d})
        
        for s in self.contained_sources:
            for k,dl in s.deck_by_case().items():
                deck_index[k].extend(dl)
        
        if source_index:
            def deck_rank(d):
                for s in source_index:
                    if d['deck'] in s['source'].contained_decks:
                        d['rank'] = s['rank']
                        return s['rank']
            
            deck_index = {k: sorted(d_list, 
                                    key = lambda d: d.get('rank') or deck_rank(d), 
                                    reverse=True)
                    for k,d_list in deck_index.items()}
        
        if as_dict:
            format_key = lambda k: '{} {}'.format(
                k[0].strftime('%Y-%m-%d'), 
                ('com' if k[1] else 'sem')+' rede')
            
            for d_list in deck_index.values():
                for d in d_list:
                    d['deck'] = d['deck'].to_dict()
            return {format_key(k): d_list
                    for k,d_list in deck_index.items()}
        
        return deck_index
    
    def source_stat(self, level=0):
        source_stat = [{
            'level': level,
            'count': len(self.contained_decks),
            'name': self.base_name(),
            'key': self.key(),
            'source': self,
        }]
        for s in self.contained_sources:
            source_stat.extend(s.source_stat(level+1))
        return source_stat
    
    def rank_sources(self, source_rank):
        source_stat = self.source_stat()
        max_level = max([s['level'] for s in source_stat])
        
        for s in source_stat:
            s['rank'] = (max_level - s['level']) * source_rank.get('level',0)
            
            pref_names = source_rank.get('name')
            if pref_names:
                _similar = lambda a,b: SequenceMatcher(a=a,b=b).ratio()
                path_as_list = s['source'].path_as_list()
                name_rank = 0
                for nm,w in pref_names.items():
                    for path_part in path_as_list:
                        name_rank = max(name_rank, _similar(path_part, nm) * w)
                s['rank'] += name_rank
        
        return source_stat
    
    def list_file_patterns(self):
        deck_type_re = 'D(?:S|ES)(?:_(?P<deck_type>ONS|CCEE))?'
        month_re = '(?P<mes>[0-9]{2})(?P<ano>[0-9]{4})'
        
        base_patterns = [
            '_?'.join([deck_type_re, month_re])
        ]
        prefix_re = '(?:(?P<prefix>[a-zA-Z0-9]*)_)?'
        sufix_re = '(?:_(?P<sufix>[a-zA-Z0-9]*))?'
        return [prefix_re + b + sufix_re for b in base_patterns]
    
    def capture_pmo_metadata(self):
        dn = self.base_name()
        for fp in self.list_file_patterns():
            m = re.match(fp, dn, re.IGNORECASE)
            if not m:
                continue
            md = {}
            for k in m.re.groupindex.keys():
                if k in ['mes','ano']:
                    v = int(m.group(k))
                else:
                    v = m.group(k)
                md[k] = v
            
            self.metadata = md
            return True
    
    def to_dict(self, level=0, detailed=False):
        d = {
            'class': self.__class__.__name__,
            'metadata': self.metadata,
            #'valid': self.valid,
            'available_decks': [d.to_dict(detailed) for d in self.contained_decks],
            }
        if level > 0:
            d.update({
                'available_sources': [s.to_dict(level-1) for s in self.contained_sources]
            })
        return d

class PmoDessemDirSource(PmoDessemSource, DirSource):
    
    def __init__(self, source_path):
        DirSource.__init__(self, source_path)
        PmoDessemSource.__init__(self)
    
    def pmo_name(self):
        return os.path.basename(self.source_path)
    
    def path_as_list(self):
        return [p for p in self.source_path.split('/') if p]
    
    def tempdir(self):
        return os.path.join(self.source_path, 'temp')
    
    def new_deck_source(self, inner_path):
        fp = os.path.join(self.source_path, inner_path)
        if os.path.isdir(fp) and fp != self.tempdir():
            return DeckDessemDirSource.detect(fp)
        if os.path.isfile(fp) and zipfile.is_zipfile(fp):
            return DeckDessemZippedSource.detect(fp)
    
    def new_pmo_source(self, inner_path):
        fp = os.path.join(self.source_path, inner_path)
        if os.path.isdir(fp):
            return PmoDessemDirSource(fp)
        if os.path.isfile(fp) and zipfile.is_zipfile(fp):
            return PmoDessemZippedSource(fp)
    
    def list_source_contents(self):
        return self.list_all()
    
    def to_dict(self):
        d = DirSource.to_dict(self)
        d.update(PmoDessemSource.to_dict(self))
        return d

class PmoDessemZippedSource(PmoDessemSource, ZippedSource):
    
    def __init__(self, zip_file_path, zip_dir=None):
        ZippedSource.__init__(self, zip_file_path, zip_dir)
        PmoDessemSource.__init__(self)
    
    def pmo_name(self):
        return os.path.basename(self.source_path)
    
    def path_as_list(self):
        return [p for p in self.zip_file_path.split('/') if p] + self.zip_dir
    
    def tempdir(self):
        base_path = os.path.dirname(self.zip_file_path)
        return os.path.join(base_path, 'temp')
    
    def new_deck_source(self, inner_path):
        if inner_path.endswith('.zip'):
            return DeckDessemInnerZippedSource.detect(
                    self.zip_file_path, 
                    inner_path)
        
        return DeckDessemZippedSource.detect(
            self.zip_file_path, 
            inner_path)
    
    def new_pmo_source(self, inner_path):
        return PmoDessemZippedSource(
            self.zip_file_path, 
            self.zip_dir + self.break_path(inner_path))
    
    def list_source_contents(self):
        return self.list_all()
    
    def to_dict(self):
        d = ZippedSource.to_dict(self)
        d.update(PmoDessemSource.to_dict(self))
        return d

class DeckDessemSource:
    
    def __init__(self):
        self.metadata = {}
        self.valid = None
    
    def is_result(self):
        return self.valid['result']
    
    def case_key(self):
        d = self.metadata
        return (date(d['ano'], d['mes'], d['dia']), d['rede'])
    
    def required_ds_files(self, files_type):
        if files_type == 'result':
            return ResultLoader.required_files()
        elif files_type == 'data':
            return Loader.required_files()
    
    def all_ds_files(self, files_type=None):
        if files_type is None:
            return self.all_ds_files('data') + self.all_ds_files('result')
        if files_type == 'result':
            return ResultLoader.all_files()
        elif files_type == 'data':
            return Loader.all_files()
    
    def file_match(self, f, file_key):
        if f.upper().startswith(file_key.upper()):
            return True
        return False
    
    def get_file_key(self, filename):
        for fk in self.all_ds_files():
            if self.file_match(filename, fk):
                return fk
    
    def search_files(self, file_key):
        f_list = self.list_files_name()
        f_found = []
        for f in f_list:
            if self.file_match(f, file_key):
                f_found.append(f)
        return f_found 
    
    def file_map(self):
        fm = defaultdict(dict)
        for ft in ['data','result']:
            if not self.valid[ft]:
                continue
            for fk in self.all_ds_files(ft):
                f_list = self.search_files(fk)
                if len(f_list):
                    fm[ft][fk] = f_list
        return fm
    
    def validate(self):
        self.valid = dict()
        for ft in ['data','result']:
            self.valid[ft] = True
            for file_key in self.required_ds_files(ft):
                if not len(self.search_files(file_key)):
                    self.valid[ft] = False
        
        if not any(self.valid.values()):
            return False
        if not self.capture_deck_metadata():
            return False
        return True
    
    def list_file_patterns(self):
        deck_type_re = 'D(?:S|ES)_(?P<deck_type>ONS|CCEE)'
        date_re = '(?P<ano>[0-9]{4})(?P<mes>[0-9]{2})(?P<dia>[0-9]{2})'
        month_re = '(?P<mes>[0-9]{2})(?P<ano>[0-9]{4})'
        rev_re = '(?:RV(?P<rev>[0-9]{1}))?' # opcional
        day_re = 'D(?P<dia>[0-9]{2})'
        rede_re = '(?:(?P<rede>SEM|COM)_?REDE)?' # opcional
        
        base_patterns = [
            '_?'.join([deck_type_re, month_re, rede_re, rev_re, day_re]),
            '_?'.join([deck_type_re, date_re, rede_re]),
        ]
        prefix_re = '(?:(?P<prefix>[a-zA-Z0-9]*)_)?'
        sufix_re = '(?:_(?P<sufix>[a-zA-Z0-9]*))?'
        return [prefix_re + b + sufix_re for b in base_patterns]
    
    def capture_deck_metadata(self):
        def adapt_rede(r):
            if r is None:
                return None
            r = r.lower()
            if r == 'sem': return False
            if r == 'com': return False
        
        dn = self.base_name()
        for fp in self.list_file_patterns():
            m = re.match(fp, dn, re.IGNORECASE)
            if not m:
                continue
            md = {}
            for k in m.re.groupindex.keys():
                if k == 'rede':
                    v = adapt_rede(m.group(k))
                elif k in ['dia','mes','ano','rev']:
                    v = int(m.group(k))
                else:
                    v = m.group(k)
                md[k] = v
            
            dt = md.get('deck_type')
            if dt and md['rede'] is None:
                md['rede'] = dt.upper() == 'ONS'
            self.metadata = md
            if self.check_deck_metadata() is False:
                return False
            return True
    
    def check_deck_metadata(self):
        args = [self.metadata.get(k) for k in ['dia','mes','ano']]
        if not all([a is not None for a in args]):
            return None
        d,m,y = args
        deck_date = None
        try:
            deck_date = date(y,m,d)
        except:
            getLogger().info('Invalid deck date: {}-{}-{}'.format(y,m,d))
        
        rev = self.metadata.get('rev')
        if rev:
            rd = real_date(rev, d, m, y)
            if rd is not None:
                if rd != deck_date:
                    getLogger().info('Deck date fixed: from {} to {}'.format(deck_date, rd))
                    self.metadata.update({'dia': rd.day, 'mes': rd.month, 'ano': rd.year})
                    deck_date = rd
                return True
        
        if deck_date is None:
            return False
        return True
    
    def to_dict(self, detailed=False):
        d = {
            'class': self.__class__.__name__,
            'metadata': self.metadata,
            'valid': self.valid
            }
        if detailed:
            d['available_files'] = self.file_map()
        return d

class DeckDessemDirSource(DeckDessemSource, DirSource):
    
    def __init__(self, source_path):
        DirSource.__init__(self, source_path)
        DeckDessemSource.__init__(self)
    
    def to_dict(self, detailed=False):
        d = DirSource.to_dict(self)
        d.update(DeckDessemSource.to_dict(self, detailed))
        return d
    
    @classmethod
    def detect(cls, source_path):
        d = cls(source_path)
        if not d.validate():
            return None
        return d

class DeckDessemZippedSource(DeckDessemSource, ZippedSource):
    
    def __init__(self, zip_file_path, zip_dir):
        ZippedSource.__init__(self, zip_file_path, zip_dir)
        DeckDessemSource.__init__(self)
    
    def make_available(self, base_dir, file_filter):
        target_dir = os.path.join(base_dir, self.base_name())
        os.makedirs(target_dir, exist_ok=True)
        
        for fn in self.z.namelist():
            if file_filter:
                fk = self.get_file_key(fn)
                if fk not in file_filter:
                    continue
            getLogger().debug('Extracting {} from {} to {}'.format(fn, self.zip_file_path, target_dir))
            self.z.extract(fn, target_dir)
        
        return DeckDessemDirSource.detect(target_dir)
    
    def to_dict(self, detailed=False):
        d = ZippedSource.to_dict(self)
        d.update(DeckDessemSource.to_dict(self, detailed))
        return d
    
    @classmethod
    def detect(cls, zip_file_path, zip_dir=None):
        if not zipfile.is_zipfile(zip_file_path):
            return None
        d = cls(zip_file_path, zip_dir)
        if not d.validate():
            return None
        return d

class DeckDessemInnerZippedSource(DeckDessemSource, InnerZippedSource):
    
    def __init__(self, zip_file_path, zip_dir):
        InnerZippedSource.__init__(self, zip_file_path, zip_dir)
        DeckDessemSource.__init__(self)
    
    def is_result(self):
        p = self.metadata.get('prefix')
        if not p:
            return False
        return p.lower().startswith('result')
    
    def inner_zip_path(self):
        return '/'.join(self.zip_dir)
    
    def make_available(self, target_dir):
        inner_path = self.inner_zip_path()
        getLogger().debug('Extracting {} from {} to {}'.format(inner_path, self.zip_file_path, target_dir))
        self.z.extract(inner_path, target_dir)
        fp = os.path.join(target_dir, inner_path)
        return DeckDessemZippedSource.detect(fp)
    
    def validate(self):
        if not self.capture_deck_metadata():
            return False
        return True
    
    def to_dict(self, detailed=False):
        d = InnerZippedSource.to_dict(self)
        d.update(DeckDessemSource.to_dict(self, detailed))
        return d
    
    @classmethod
    def detect(cls, zip_file_path, zip_dir):
        if not zipfile.is_zipfile(zip_file_path):
            return None
        d = cls(zip_file_path, zip_dir)
        if not d.validate():
            return None
        return d

def getLogger():
    return logging.getLogger(__name__)
