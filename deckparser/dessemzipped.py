'''
Created on 2 de nov de 2018

@author: Renan Maciel
'''
import zipfile, os, re, shutil
from uuid import uuid4 as hasher
from datetime import date
import logging

class DessemZipped(object):
    def __init__(self, fn=None):
        # arquivo zipado que sera aberto
        self.z = None
        self.dias = dict()
        self.dirname = None
        self.zipfilename = None
        self.filename = None
        self.fhash = None
        self.internal_dir = None
        if fn:
            self.setZipFile(fn)
            self.setFilePattern(1)
            self.openZip()
            if len(self.dias) == 0:
                self.setFilePattern(2)
                self.openZip()
        else:
            self.fn = None

    def getLogger(self):
        return logging.getLogger(__name__)

    def __del__(self):
        for d in self.dias:
            for r in self.dias[d]:
                if self.dias[d][r]['zip'] is not None:
                    self.closeDia(d, r)
        if self.z:
            self.z.close()

    def zipLoaded(self):
        if self.z:
            return True
        else:
            return False

    def setZipFile(self,fn):
        self.fn = fn
        
    def setFilePattern(self, cod):
        if cod == 1:
            self.fileReExpr = "DES_CCEE_([0-9]{4})([0-9]{2})([0-9]{2})_(Sem|Com)Rede.zip"
            self.fileParseFunc = DessemZipped.parseFileNamePat1
        elif cod == 2:
            self.fileReExpr = "DS_CCEE_([0-9]{2})([0-9]{4})_(SEM|COM)REDE_RV([0-9]{1})D([0-9]{2}).zip"
            self.fileParseFunc = DessemZipped.parseFileNamePat2
        else:
            raise ValueError('Invalid file pattern code: '+str(cod))
    
    @staticmethod
    def parseFileNamePat1(rr):
        r = True if rr.group(4) == 'Com' else False
        return {'ano': int(rr.group(1)), 'mes': int(rr.group(2)), 'dia': int(rr.group(3)), 'rede': r}
    
    @staticmethod
    def parseFileNamePat2(rr):
        r = True if rr.group(3) == 'COM' else False
        d = int(rr.group(5))
        m = int(rr.group(1))
        rv = int(rr.group(4))
        if rv == 0 and d > 20:
            m = m - 1
        elif rv > 3 and d < 10:
            m = m + 1
        return {'ano': int(rr.group(2)), 'mes': m, 'dia': d, 'rede': r, 'rv': rv}

    def openZip(self):
        if zipfile.is_zipfile(self.fn):
            self.z = zipfile.ZipFile(self.fn, 'r')
            real_path = os.path.realpath(self.fn)
            self.dirname = os.path.dirname(real_path)
            self.zipfilename = real_path.split("/")[-1]
            self.filename = self.zipfilename.split(".")[-2]
            self.fhash = str(hasher())
            for fn in self.z.namelist():
                rr = re.match(self.fileReExpr,fn)
                if rr is None:
                    self.getLogger().info('File ignored: %s', fn)
                    continue
                self.getLogger().info('File indexed: %s', fn)
                ps = self.fileParseFunc(rr)
                d = date(ps['ano'], ps['mes'], ps['dia'])
                r = ps['rede']
                if d:
                    if d not in self.dias: self.dias[d] = {}
                    self.dias[d][r] = {
                        'filename': fn,
                        'zip': None,
                        'tmpdir': None,
                        'filelist': dict()
                    }
        else:
            self.getLogger().error('%s is not a zip file', self.fn)
            
    def getDate(self, dia):
        for d in self.dias:
            if d.day == dia:
                return d
    
    def printIndex(self):
        print('\nAvailable cases\n')
        itm = []
        for d in self.dias:
            for r in self.dias[d]:
                itm.append((d,r))
        itm.sort()
        for i in itm:
            (d, r) = i
            rd = 'Com rede' if r else 'Sem rede'
            print(d.strftime('%d/%b/%Y') + ', ' + rd)

    def extractAllFiles(self,dia,r):
        try:
            d = self.dias[dia][r]
            if d['zip'] is None:
                self.openDia(dia, r)
            for f in d['filelist']:
                fname = d['filelist'][f]
                z = d['zip']
                z.extract(fname, d['tmpdir'])
            return d['tmpdir']
        except:
            rd = 'Com rede' if r else 'Sem rede'
            self.getLogger().warning('Error unziping file %s, case: %s %s', f, str(dia), str(rd))
            raise

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
        
            fname = d['filename']
            self.z.extract(fname, tmpdir)
            
            fPath = os.path.join(tmpdir, fname)
            d['zip'] = zipfile.ZipFile(fPath,'r')
            for fn in d['zip'].namelist():
                f = fn.split('.')[0].upper()
                d['filelist'][f] = fn
            d['tmpdir'] = tmpdir
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
            d['filelist'] = dict()
            d['tmpdir'] = None
            shutil.rmtree(tmpdir)
        except:
            self.getLogger().warning('Error closing day: %s', str(dia))
            raise
