'''
Created on 2 de nov de 2018

@author: Renan Maciel
'''
import zipfile, os, re, shutil
from uuid import uuid4 as hasher
from datetime import date
import logging

def dessem_source(fn, open_results=False, pmo_date=None):
    if os.path.isdir(fn):
        return DessemDir(fn, open_results, pmo_date)
    if zipfile.is_zipfile(fn):
        return DessemZipped(fn, open_results, pmo_date)

class DessemFilePattern:
    def __init__(self, rex, open_results, pmo_date):
        self.fileReExpr = rex
        self.open_results = open_results
        self.pmo_date = pmo_date
    
    def matchFileName(self, fn):
        return re.match(self.getRegex(),fn)
    
    def decodeFileName(self, fn):
        m = self.matchFileName(fn)
        if m:
            return self.capture(m)
    
    def realMonth(self, rv, d, m, y):
        if rv == 0 and d > 20:
            m = m - 1
            if m < 1:
                m = 12
                y = y - 1
        elif rv > 3 and d < 10:
            m = m + 1
            if m > 12:
                m = 1
                y = y + 1
        return m,y
    
    def realDate(self, rv, d, m, y):
        m,y = self.realMonth(rv, d, m, y)
        try:
            return date(y,m,d)
        except:
            raise ValueError('Invalid deck date: {:d}-{:d}-{:d} rv {:d}'.format(y,m,d,rv))
    
    def getLogger(self):
        return logging.getLogger(__name__)

class DessemFilePattern_CCEE(DessemFilePattern):
    def __init__(self, *args, **kwargs):
        self.sub_dir = kwargs.pop('sub_dir', None)
        super().__init__(*args, **kwargs)
    
    def getRegex(self):
        rex = self.fileReExpr
        if self.open_results:
            rex = "Resultado_" + rex
        if self.sub_dir:
            rex = self.sub_dir + '/' + rex
        return rex

class DessemFilePattern_CCEE1(DessemFilePattern_CCEE):
    def __init__(self, open_results, pmo_date, sub_dir=None):
        super().__init__("DES_CCEE_([0-9]{4})([0-9]{2})([0-9]{2})_(Sem|Com)Rede.zip", 
                         open_results, pmo_date, sub_dir=sub_dir)
    
    def capture(self, rr):
        r = True if rr.group(4) == 'Com' else False
        return {'ano': int(rr.group(1)), 'mes': int(rr.group(2)), 'dia': int(rr.group(3)), 'rede': r}

class DessemFilePattern_CCEE2(DessemFilePattern_CCEE):
    def __init__(self, open_results, pmo_date, sub_dir=None):
        super().__init__("DS_CCEE_([0-9]{2})([0-9]{4})_(SEM|COM)REDE_RV([0-9]{1})D([0-9]{2})_?([A-Z]*).zip", 
                         open_results, pmo_date, sub_dir=sub_dir)
    
    def capture(self, rr):
        r = True if rr.group(3) == 'COM' else False
        d = int(rr.group(5))
        m = int(rr.group(1))
        y = int(rr.group(2))
        rv = int(rr.group(4))
        sufix = rr.group(6)
        dt = self.realDate(rv, d, m, y)
        return {'ano': dt.year, 'mes': dt.month, 'dia': dt.day, 'rede': r, 'rv': rv, 'sufix': sufix}

class DessemFilePattern_ONS(DessemFilePattern):
    def __init__(self, open_results, pmo_date):
        super().__init__("DS_ONS_([0-9]{2})([0-9]{4})_RV([0-9]{1})D([0-9]{2}).zip", open_results, pmo_date)
    
    def getRegex(self):
        return self.fileReExpr
    
    def capture(self, rr):
        r = True
        d = int(rr.group(4))
        m = int(rr.group(1))
        y = int(rr.group(2))
        rv = int(rr.group(3))
        dt = self.realDate(rv, d, m, y)
        return {'ano': dt.year, 'mes': dt.month, 'dia': dt.day, 'rede': r, 'rv': rv}

class DessemSource(object):
    def __init__(self, fn=None, open_results=False, pmo_date=None):
        self.dias = dict()
        self.dirname = None
        self.fhash = None
        self.sourceValid = False
        self.pmo_date = pmo_date
        self.open_results = open_results
        if fn:
            self.setSource(fn)
            if not self.checkSource():
                self.fn = None
                return
            if not self.pmo_date:
                self.getLogger().warn('PMO date not provided, deck dates will not be fixed')
            for fp in self.sourceFilePatternList():
                self.scanSource(fp)
                if len(self.dias) > 0:
                    self.sourceValid = True
                    break
        else:
            self.fn = None

    def getLogger(self):
        return logging.getLogger(__name__)

    def setSource(self,fn):
        self.fn = fn
    
    def validSource(self):
        return self.sourceValid
    
    def scanSource(self, fp):
        self.fhash = str(hasher())
        fList = self.getFileNameList()
        for fn in fList:
            if not fp.matchFileName(fn):
                self.getLogger().debug('File ignored: %s', fn)
                continue
            self.getLogger().debug('File indexed: %s', fn)
            ps = fp.decodeFileName(fn)
            d = date(ps['ano'], ps['mes'], ps['dia'])
            r = ps['rede']
            if d:
                if d not in self.dias: self.dias[d] = {}
                self.dias[d][r] = {
                    'filename': fn,
                    'zip': None,
                    'tmpdir': None,
                    'filelist': []
                }
    
    def getDate(self, dia):
        for d in self.dias:
            if d.day == dia:
                return d
    
    def printIndex(self):
        print('\nAvailable cases\n')
        itm = self.listIndex()
        for d,r in itm:
            rd = 'Com rede' if r else 'Sem rede'
            print(d.strftime('%d/%b/%Y') + ', ' + rd)
    
    def listIndex(self):
        itm = []
        for d in self.dias:
            for r in self.dias[d]:
                itm.append((d,r))
        itm.sort()
        return itm
    
    def extractAllFiles(self,dia,r):
        fList = self.dias[dia][r]['filelist']
        return self.extractFiles(dia, r, fList)
    
    def extractFiles(self,dia,r,fileList):
        try:
            d = self.dias[dia][r]
            if d['zip'] is None:
                self.openDia(dia, r)
            for f in fileList:
                rf_list = self.listRealFiles(f, d['filelist'])
                if len(rf_list):
                    for fname in rf_list:
                        z = d['zip']
                        z.extract(fname, d['tmpdir'])
                else:
                    rd = 'Com rede' if r else 'Sem rede'
                    self.getLogger().warning('Absent file %s, case: %s %s', f, str(dia), rd)
            return d['tmpdir']
        except:
            rd = 'Com rede' if r else 'Sem rede'
            self.getLogger().warning('Error unziping file %s, case: %s %s', f, str(dia), rd)
            raise
    
    def listRealFiles(self, f, realFileList):
        fList = []
        f = f.upper()
        for rf in realFileList:
            if rf.upper().startswith(f):
                fList.append(rf)
        return fList
    
    def openDia(self, dia, r):
        try:
            if dia not in self.dias:
                raise ValueError('Date not indexed: '+str(dia))
            if r not in self.dias[dia]:
                raise ValueError('Grid option not available: '+str(r))
            
            d = self.dias[dia][r]
            if d['zip'] is not None:
                return
            
            tmpdir = os.path.join(self.dirname, 'temp')
            if not os.path.exists(tmpdir):
                os.mkdir(tmpdir)
            rd = 'ComRede' if r else 'SemRede'
            tmpdir = os.path.join(tmpdir, self.fhash+'_dia'+str(dia)+rd)
            os.mkdir(tmpdir)
        
            self.extractDia(d, tmpdir)
            
            for fn in d['zip'].namelist():
                d['filelist'].append(fn)
            return tmpdir
        except:
            self.getLogger().error('Error opening day: %s', str(dia))
            raise
    
    def closeDia(self, dia, r):
        try:
            d = self.dias[dia][r]
            tmpdir = d['tmpdir']
            del d['zip']
            d['zip'] = None
            d['filelist'] = []
            d['tmpdir'] = None
            shutil.rmtree(tmpdir)
        except:
            self.getLogger().warning('Error closing day: %s', str(dia))
            raise

    def __del__(self):
        for d in self.dias:
            for r in self.dias[d]:
                if self.dias[d][r]['zip'] is not None:
                    self.closeDia(d, r)
    
class DessemZipped(DessemSource):
    
    def __init__(self, *args, **kwargs):
        self.preferred_subdir = kwargs.pop('preferred_subdir', 'Reprocessamento')
        self.subdir = None
        super().__init__(*args, **kwargs)
    
    def sourceFilePatternList(self):
        return [DessemFilePattern_CCEE1(self.open_results, self.pmo_date, sub_dir=self.subdir), 
                DessemFilePattern_CCEE2(self.open_results, self.pmo_date, sub_dir=self.subdir)]
    
    def checkSource(self):
        if zipfile.is_zipfile(self.fn):
            self.z = zipfile.ZipFile(self.fn, 'r')
            real_path = os.path.realpath(self.fn)
            self.dirname = os.path.dirname(real_path)
            self.zipfilename = os.path.basename(real_path)
            self.subdir = self.getSubdir()
            if self.subdir:
                self.getLogger().info('Using zip inner directory: {:s}'.format(self.subdir))
            if not self.pmo_date:
                self.detectPmoDate()
            return True
        else:
            self.getLogger().error('%s is not a zip file', self.fn)
            return False
    
    def detectPmoDate(self):
        rex = "(DES|des)_([0-9]{4})([0-9]{2}).zip"
        mt = re.match(rex, self.zipfilename)
        if mt:
            self.pmo_date = date(int(mt.group(2)), int(mt.group(3)), 1)
            self.getLogger().info('Detected PMO date: ' + self.pmo_date.isoformat())
    
    def extractDia(self, d, tmpdir):
        fname = d['filename']
        self.z.extract(fname, tmpdir)
        fPath = os.path.join(tmpdir, fname)
        d['zip'] = zipfile.ZipFile(fPath,'r')
        d['tmpdir'] = tmpdir
    
    def matchAnyFilePattern(self, file_name):
        for fp in self.sourceFilePatternList():
            if fp.matchFileName(file_name):
                return True
    
    def getSubdir(self):
        zip_dirs = [info for info in self.z.infolist() if info.is_dir()]
        if len(zip_dirs) == 0:
            return None
        
        pref_dir = self.preferred_subdir
        if pref_dir:
            for d in zip_dirs:
                dn = d.filename[:-1]
                if dn == pref_dir:
                    return dn
        
        zip_files = [info for info in self.z.infolist() if not info.is_dir()]
        if any([self.matchAnyFilePattern(info.filename) 
                for info in zip_files]):
            return None
        return zip_dirs[0].filename[:-1]
    
    def getFileNameList(self):
        return self.z.namelist()
    
    def __del__(self):
        super().__del__()
        if self.z:
            self.z.close()

class DessemDir(DessemSource):
    
    def sourceFilePatternList(self):
        return [DessemFilePattern_ONS(self.open_results, self.pmo_date)]
    
    def checkSource(self):
        if os.path.isdir(self.fn):
            self.dirname = os.path.realpath(self.fn)
            return True
        else:
            self.getLogger().error('%s is a invalid directory', self.fn)
            return False
    
    def extractDia(self, d, tmpdir):
        fname = d['filename']
        fPath = os.path.join(self.dirname, fname)
        d['zip'] = zipfile.ZipFile(fPath,'r')
        d['tmpdir'] = tmpdir
    
    def getFileNameList(self):
        fList = []
        for f in os.listdir(self.dirname):
            fp = os.path.join(self.dirname, f)
            if os.path.isfile(fp):
                fList.append(f)
        return fList
