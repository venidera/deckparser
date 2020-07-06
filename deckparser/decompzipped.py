import zipfile, os, re, shutil
from uuid import uuid4 as hasher
from datetime import datetime
from logging import info,debug
from os.path import realpath,dirname

class DecompZipped(object):
    def __init__(self, fn=None,r_fn=None):
        # arquivo zipado que sera aberto
        self.z = None
        self.sem = dict()
        self.relatorio = dict()
        self.dirname = None
        self.zipfilename = None
        self.filename = None
        self.fhash = None
        self.internal_dir = None
        self.fn = None
        self.r_fn = None
        if fn:
            self.fn = fn
            if r_fn:
                self.r_fn = r_fn
            self.openZip()

    def __del__(self):
        for key in self.sem:
            if self.sem[key]['zip'] is not None:
                self.closeSemana(key)
        if self.z:
            self.z.close()

    def zipLoaded(self):
        if self.z:
            return True
        else:
            return False


    def openZip(self):
        self.z = zipfile.ZipFile(self.fn, 'r')
        real_path = os.path.realpath(self.fn)
        self.dirname = os.path.dirname(real_path)
        self.zipfilename = real_path.split("/")[-1]
        self.filename = self.zipfilename.split(".")[-2]

        if self.r_fn:
            self.r_z = zipfile.ZipFile(self.r_fn,'r')
            real_path = os.path.realpath(self.r_fn)
            self.r_dirname = os.path.dirname(real_path)
            self.r_zipfilename = real_path.split("/")[-1]
            self.r_filename = self.r_zipfilename.split(".")[-2]

        self.fhash = str(hasher())

        def init_sem(sem):
            if sem not in self.sem:
                self.sem[sem] = {
                    'filename': None,
                    'relfilename': None,
                    'zip': None,
                    'filelist': dict(),
                    'relzip': None,
                    'relfilelist': dict(),
                    'tmpdir': None,
                }
        namelist = self.z.namelist()

        for fn in namelist:
            if fn.lower()=='caso.dat':
                init_sem(1)
                self.sem[1]['zip'] = self.z
                self.openDeckONS()
                break
            sem = re.search(re.escape(self.filename)+"\-sem([1234]).zip",fn)
            if sem:
                init_sem(int(sem.group(1)))
                self.sem[int(sem.group(1))]['filename'] = fn
            else:
                rel = re.search("Relatorio_Sumario\-[0-9]+\-sem([1234]).zip",fn)
                if rel:
                    init_sem(int(rel.group(1)))
                    self.sem[int(rel.group(1))]['relfilename'] = fn


    def numSemanas(self):
        return len(self.sem)

    def openDeckONS(self):
        tmpdir = self.dirname+"/"+self.fhash
        os.mkdir(tmpdir)

        for fn in self.sem[1]['zip'].namelist():
            tag = fn.split('.')[0].upper()
            self.sem[1]['filelist'][tag] = fn
        if self.r_fn:
            self.sem[1]['relzip'] = zipfile.ZipFile(self.r_fn,'r')
            for fn in self.sem[1]['relzip'].namelist():
                tag = fn.split('.')[0].upper()
                self.sem[1]['relfilelist'][tag] = fn

        self.sem[1]['tmpdir'] = tmpdir

    def openSemana(self,num_sem):
        try:
            if num_sem not in self.sem:
                raise ValueError('Deck não possui a semana especificada')

            if self.sem[num_sem]['zip'] is not None:
                return

            tmpdir = self.dirname+"/"+self.fhash+'_sem'+str(num_sem)
            os.mkdir(tmpdir)

            fname = self.sem[num_sem]['filename']
            relfname = self.sem[num_sem]['relfilename']
            self.z.extract(fname, tmpdir)
            self.sem[num_sem]['zip'] = zipfile.ZipFile(tmpdir+'/'+fname,'r')
            for fn in self.sem[num_sem]['zip'].namelist():
                tag = fn.split('.')[0].upper()
                self.sem[num_sem]['filelist'][tag] = fn
            if relfname:
                self.z.extract(relfname, tmpdir)
                self.sem[num_sem]['relzip'] = zipfile.ZipFile(tmpdir+'/'+
                                                              relfname,'r')
                for fn in self.sem[num_sem]['relzip'].namelist():
                    tag = fn.split('.')[0].upper()
                    self.sem[num_sem]['relfilelist'][tag] = fn

            self.sem[num_sem]['tmpdir'] = tmpdir
        except:
            info('Erro ao abrir semana',num_sem)
            raise


    def closeSemana(self,num_sem):
        try:
            tmpdir = self.sem[num_sem]['tmpdir']
            shutil.rmtree(tmpdir)
            del self.sem[num_sem]['zip']
            if self.sem[num_sem]['relzip']:
                del self.sem[num_sem]['relzip']
            self.sem[num_sem]['zip'] = None
            self.sem[num_sem]['relzip'] = None
            self.sem[num_sem]['filelist'] = dict()
            self.sem[num_sem]['relfilelist'] = dict()
            self.sem[num_sem]['tmpdir'] = None
        except:
            info('Erro ao fechar semana ',num_sem)
            raise

    def openFile(self,num_sem,tag):
        try:
            if self.sem[num_sem]['zip'] is None:
                self.openSemana(num_sem)
            if tag in self.sem[num_sem]['filelist']:
                fname = self.sem[num_sem]['filelist'][tag]
                z = self.sem[num_sem]['zip']
            elif tag in self.sem[num_sem]['relfilelist']:
                fname = self.sem[num_sem]['relfilelist'][tag]
                z = self.sem[num_sem]['relzip']
            f = z.open(fname)
            return f
        except:
            info('Erro ao abrir',fnp)
            raise

    def openFileExtData(self,num_sem,tag):
        try:
            if self.sem[num_sem]['zip'] is None:
                self.openSemana(num_sem)
            if tag in self.sem[num_sem]['filelist']:
                fname = self.sem[num_sem]['filelist'][tag]
                z = self.sem[num_sem]['zip']
            elif tag in self.sem[num_sem]['relfilelist']:
                fname = self.sem[num_sem]['relfilelist'][tag]
                z = self.sem[num_sem]['relzip']
            else:
                raise ValueError('Tag {} não encontrado'.format(tag))
            z.extract(fname, self.sem[num_sem]['tmpdir'])

            filepath = self.sem[num_sem]['tmpdir']+'/'+fname
            f = open(filepath,'r',encoding='latin_1')
            data = f.readlines()
            f.close()
            os.remove(filepath)
            return data
        except:
            info('Erro ao extrair arquivo ',num_sem,tag)
            raise

    def extractFile(self,num_sem,tag):
        try:
            if self.sem[num_sem]['zip'] is None:
                self.openSemana(num_sem)
            if tag in self.sem[num_sem]['filelist']:
                fname = self.sem[num_sem]['filelist'][tag]
                z = self.sem[num_sem]['zip']
            elif tag in self.sem[num_sem]['relfilelist']:
                fname = self.sem[num_sem]['relfilelist'][tag]
                z = self.sem[num_sem]['relzip']
            else:
                raise ValueError('Tag {} não encontrado'.format(tag))
            e = z.extract(fname, self.sem[num_sem]['tmpdir'])
            return self.sem[num_sem]['tmpdir']+'/'+fname
        except:
            info('Erro ao extrair arquivo ',num_sem,tag)
            raise
