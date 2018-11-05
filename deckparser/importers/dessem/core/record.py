'''
Created on 4 de jul de 2018

@author: Renan
'''
import re
from deckparser.importers.dessem.core.dataType import parseDataType, validateDataType

class record:
    
    def __init__(self, recMap):
        self.recMap = recMap
        self.data = None
        self.line = None
        
    def isEmpty(self):
        return self.data is None
     
    def toDict(self, df=True):
        ds = {}
        r = self.data
        if r is None:
            return ds
        if df:
            return self.applyDefault(r)
        for k in self.recMap:
            f = self.recMap[k]
            if f['composed']:
                for kd in record.composedToDict(f, r):
                    ds[kd] = r.get(kd)
            else:
                ds[k] = r.get(k)
        return ds
    
    @staticmethod
    def composedToDict(f, r):
        refKey = r.get(f['refField'])
        fields = f['set'][refKey]
        ds = {}
        for kd in fields:
            ds[kd] = r.get(kd)
        return ds
    
    def clear(self):
        self.data = None
        self.metadata = None
        self.line = None
        
    @staticmethod
    def infnity(size):
        return 10**size - 1
    
    @staticmethod
    def isComment(line):
        return line[0] == '&'
    
    @staticmethod
    def assertString(line, s):
        return line.strip() == s
    
    @staticmethod
    def isBlankLine(line):
        return line.strip() == ''
    
    @staticmethod
    def isEOF(line):
        return record.assertString(line, 'FIM')
    
    def isBlankField(self, v):
        return v.strip() == ''
    
    def addField(self, name, cfg):
        self.recMap[name] = cfg
        
    def setField(self, key, v):
        self.data[key] = v
        
    def getField(self, key):
        return self.data[key]
        
    def getData(self):
        return self.data
        
    def listFields(self, reField=None):
        if reField == None:
            return self.recMap.keys()
        
        pattern = re.compile(reField)
        fl = []
        for f in self.recMap:
            if pattern.match(f) is not None:
                fl.append(f)
        return fl
    
    def showFields(self):
        for k in self.recMap:
            print('{:s}: {:s}'.format(k, str(self.recMap[k])))
    
    def setRange(self, key, r):
        self.recMap[key]['range'] = r
        
    def applyDefault(self, r):
        ds = {}
        for k in r:
            if r[k] is None:
                if k in self.recMap:
                    f = self.recMap[k]
                    if 'default' in f:
                        ds[k] = f['default']
                    else:
                        ds[k] = None
            else:
                ds[k] = r[k]
        return ds

    def parse(self, line):
        m = self.recMap
        r = dict()
        mt = dict()
        
        for key in m:
            f = m[key]
            cps = f['composed'] if 'composed' in f else False
            try:
                if cps:
                    pos = f['position']
                    refKey = r[f['refField']]
                    if refKey not in f['set']:
                        print('Missing config: {:s}'.format(refKey))
                        continue
                    fields = f['set'][refKey]
                    for kd in fields:
                        fd = fields[kd]
                        rd = [pos, pos + fd['size'] - 1]
                        vd, mtd = self.parseField(fd, rd, line)
                        if 'validate' in fd:
                            self.validateField(fd['validate'], vd)
                        r[kd] = vd
                        mt[kd] = mtd
                        pos = pos + fd['size']
                else:
                    v, mtd = self.parseField(f, f['range'], line)
                    if 'validate' in f:
                        self.validateField(f['validate'], v)
                    r[key] = v
                    mt[key] = mtd
            except (ValueError, KeyError):
                print('Line: {:s}'.format(line))
                print('Field: {:s}'.format(key))
                raise
        self.data = r
        self.metadata = mt
        self.line = line
        return r
    
    def parseField(self, f, r, line):
        t = f['type']
        v = line[r[0]-1:r[1]]
        
        md = dict()
        if v != '':
            if v[0] != ' ':
                md['just'] = 'l'
            elif v[len(v)-1] != ' ':
                md['just'] = 'r'
        
        v = v.strip()
        
        if self.isBlankField(v):
            return None, md
        
        if 'special' in f:
            s = self.readSpecial(f, v)
            if s is not None:
                return s, md
        
        value = parseDataType(v, t)
        validateDataType(value, t)
    
        if t == 'real':
            md['format'] = self.detectRealFormat(v)

        return value, md
    
    def detectRealFormat(self, v):
        i = v.find('.')
        if i < 0:
            return 0
        return len(v)-i-1
    
    def validateField(self, validate, v):
        if v is None:
            return
        
        if 'range' in validate:
            r = validate['range']
            if v < r[0] or v > r[1]:
                print('Value: {:s}, Range: [{:s}, {:s}]'.format(str(v), str(r[0]), str(r[1])))
                raise ValueError('Validation: range')
            
        if 'value' in validate:
            if v != validate['value']:
                print('Value: {:s}, Expected: {:s}'.format(str(v), str(validate['value'])))
                raise ValueError('Validation: value')
            
        if 'list' in validate:
            if v not in validate['list']:
                print('Value: {:s}, List: {:s}'.format(str(v), str(validate['list'])))
                raise ValueError('Validation: list')
            
        if 'min' in validate:
            if v < validate['min']:
                print('Value: {:s}, Min: {:s}'.format(str(v), str(validate['min'])))
                raise ValueError('Validation: min')
            
    def readSpecial(self, f, value):
        sList = f['special']
        for s in sList:
            if value.strip() == s:
                return s
        return None
    
    def isSpecial(self, f, value):
        if 'special' not in f:
            return False
        sList = f['special']
        for s in sList:
            if value == s:
                return True
        return False
    
    def show(self, showRaw=False):
        if self.data is None:
            print('<Empty Record>')
        else:
            self.showLine(self.data, self.metadata)
            if showRaw:
                print("R: " + self.line)
    
    def showLine(self, line, metadata):
        ls = ''
        pos = 1
        
        for key in self.recMap:
            f = self.recMap[key]
            cps = f['composed'] if 'composed' in f else False
            if cps:
                cpsPos = f['position']
                refKey = line[f['refField']]
                if refKey not in f['set']:
                    print('Missing config: {:s}'.format(refKey))
                    continue
                fields = f['set'][refKey]
                for kd in fields:
                    fd = fields[kd]
                    r = [cpsPos, cpsPos + fd['size'] - 1]
                    try:
                        ls = ls + ' '*(r[0] - pos - 1) + self.formatField(fd, r, line[kd], metadata[kd])
                    except ValueError:
                        print('Field: {:s}, Type: {:s}, Value: {:s}'.format(kd, fd['type'], str(line[kd])))
                        raise
                    pos = cpsPos + fd['size']
            else:
                f = self.recMap[key]
                r = f['range']
                fmtField = self.formatField(f, r, line[key], metadata[key])
                ls = ls + ' '*(r[0] - pos - 1) + fmtField
                pos = r[1]
        print("M: " + ls)
    
    def formatField(self, f, r, v, mdt):
        t = f['type']
        size = r[1] - r[0] + 1
        just = 'l'
        if 'just' in mdt:
            just = mdt['just']
        
        if v is None:
            return self.just('', size, just)
        
        if self.isSpecial(f, v):
            return self.just(v, size, just)
        
        return self.formatValue(v, t, size, just, mdt)
        
    def formatValue(self, v, t, size, just, mdt):
        if t == 'int' or t in ['h', 'd', 'ds', 'm', 'a', 'bin']:
            fmt = '{:' + str(size) + 'd}'
            return self.just(fmt.format(v), size, just)
        if t == 'real':
            inf = self.infnity(size)
            if v >= inf:
                return self.just('Inf', size, just)
            if v <= -inf:
                return self.just('-Inf', size, just)
            
            dec = 0
            if 'format' in mdt:
                dec = mdt['format']
            fmt = '{:' + str(size) + '.' + str(dec) + 'f}'
            return self.just(fmt.format(v), size, just)
        return self.just(v, size, just)
    
    def just(self, v, size, j):
        if len(v) > size:
            v = v[0:size-1]
        
        if j == 'l':
            return v.ljust(size)
        if j == 'r':
            return v.rjust(size)
        return v.ljust(size)
    