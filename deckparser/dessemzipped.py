'''
Created on 2 de nov de 2018

@author: Renan Maciel
'''
import zipfile, os, re, shutil
from uuid import uuid4 as hasher
from logging import info
from datetime import date

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
            self.openZip()
        else:
            self.fn = None

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

    def openZip(self):
        if zipfile.is_zipfile(self.fn):
            self.z = zipfile.ZipFile(self.fn, 'r')
            real_path = os.path.realpath(self.fn)
            self.dirname = os.path.dirname(real_path)
            self.zipfilename = real_path.split("/")[-1]
            self.filename = self.zipfilename.split(".")[-2]
            self.fhash = str(hasher())
            for fn in self.z.namelist():
                rr = re.match("DES_CCEE_([0-9]{4})([0-9]{2})([0-9]{2})_(Sem|Com)Rede.zip",fn)
                if rr is None:
                    print('Arquivo ignorado: '+str(fn))
                    continue
                else:
                    print('Arquivo indexado: '+str(fn))
                d = date(int(rr.group(1)), int(rr.group(2)), int(rr.group(3)))
                r = True if rr.group(4) == 'Com' else False
                if d:
                    if d not in self.dias: self.dias[d] = {}
                    self.dias[d][r] = {
                        'filename': fn,
                        'zip': None,
                        'tmpdir': None,
                        'filelist': dict()
                    }
                        
        else:
            info(self.fn + " is not a zip file")

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
            info('Erro ao extrair arquivo ',dia,f)
            raise

    def openDia(self, dia, r):
        try:
            if dia not in self.dias:
                raise ValueError('Deck nao possui o dia especificado: '+str(dia))
            if r not in self.dias[dia]:
                raise ValueError('Opcao de rede eletrica nao disponivel: '+str(r))
            
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
            info('Erro ao abrir dia',dia)
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
            info('Erro ao fechar dia ',dia)
            raise
