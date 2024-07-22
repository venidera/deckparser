import zipfile
import os
from uuid import uuid4 as hasher
from logging import info


class NewaveZipped(object):
    def __init__(self, fn=None):
        # arquivo zipado que sera aberto
        self.z = None
        self.dirname = None
        self.zipfilename = None
        self.filename = None
        self.fhash = None
        self.fns_set = None
        self.internal_dir = None
        if fn:
            self.setZipFile(fn)
            self.openZip()
        else:
            self.fn = None

    def __del__(self):
        if self.z:
            self.z.close()

    def zipLoaded(self):
        if self.z:
            return True
        else:
            return False

    def setZipFile(self, fn):
        self.fn = fn

    def openZip(self):
        if zipfile.is_zipfile(self.fn):
            self.z = zipfile.ZipFile(self.fn, 'r')
            real_path = os.path.realpath(self.fn)
            self.dirname = os.path.dirname(real_path)
            self.zipfilename = real_path.split("/")[-1]
            self.filename = self.zipfilename.split(".")[-2]
            self.fhash = str(hasher())
            self.fns_set = dict()
            for fn in self.z.namelist():
                if '/' in fn:
                    intdpath = '/'.join(fn.split('/')[0:-1]) + '/'
                    if not self.internal_dir:
                        self.internal_dir = intdpath
                    if self.internal_dir and self.internal_dir != intdpath:
                        raise Exception('Multiple directories inside a zipfile.')
                if self.internal_dir:
                    evfn = fn.split('/')[-1].split('.')[0].upper()
                else:
                    evfn = fn.split('.')[0].upper()
                if evfn == 'MODIF1':
                    key = 'MODIF'
                else:
                    key = evfn
                self.fns_set[key] = fn
            # Check if it is a deck
            deckfiles = ['dger', 'sistema', 'confh', 'confhd']
            zipfiles = list(self.fns_set.keys())
            if not all([fd.upper() in str(zipfiles) for fd in deckfiles]):
                # if not set([fd.lower() for fd in deckfiles]).issubset(set([fz.lower() for fz in zipfiles])):
                info('The file doesn\'t look like a deck file.')
                # Check if it has a zip
                possible_decks = dict()
                for kfname, fname in self.fns_set.items():
                    if '.zip' in fname.lower():
                        for obj in self.z.infolist():
                            possible_decks[obj.filename] = obj.date_time
                        break
                if len(possible_decks) > 0:
                    newer = None
                    for k, v in possible_decks.items():
                        if not newer:
                            newer = (k, v)
                        else:
                            if v > newer[1]:
                                newer = (k, v)
                    self.z.extract(newer[0], '/tmp')
                    self.setZipFile('/tmp/' + newer[0])
                    self.openZip()
                else:
                    raise Exception('The file opened is not a deck file and doesn\'t have a deck in its files.')

        else:
            info(self.fn + " is not a zip file")

    def openFile(self, fnp):
        try:
            fname = self.fns_set[fnp.upper()]
            f = self.z.open(fname)
            return f
        except Exception:
            info('Fail to open ', fnp)
            print('Fail to open ', fnp)
            return False

    def openFileExtData(self, fnp):
        try:
            fname = self.fns_set[fnp.upper()]
            self.z.extract(fname, self.dirname)
            if self.internal_dir:
                destfile = self.dirname + '/' + self.internal_dir + '/' + self.fhash + '_' + fname.split('/')[-1]
            else:
                destfile = self.dirname + "/" + self.fhash + '_' + fname
            os.rename(self.dirname + "/" + fname, destfile)
            try:
                f = open(destfile, 'r')
                data = f.readlines()
                f.close()
                os.remove(destfile)
                return data
            except:
                f = open(destfile, 'r', encoding='iso8859-1')
                data = f.readlines()
                f.close()
                os.remove(destfile)
                return data
        except Exception:
            info('Fail to extract ', fnp)
            return False

    def extractFile(self, fnp):
        try:
            fname = self.fns_set[fnp.upper()]
            self.z.extract(fname, self.dirname)
            if self.internal_dir:
                destfile = self.dirname + '/' + self.internal_dir + '/' + self.fhash + '_' + fname.split('/')[-1]
            else:
                destfile = self.dirname + "/" + self.fhash + '_' + fname
            os.rename(self.dirname + "/" + fname, destfile)
            return destfile
        except Exception:
            info('Fail to extract ', fnp)
            return False
