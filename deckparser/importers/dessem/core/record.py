'''
Created on 4 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dataType import parseDataType, validateDataType
from deckparser.importers.dessem.core.exceptions import ValidationException
import logging

class record:
    
    def __init__(self, recMap):
        self.recMap = recMap
        self.exportIgnore = ['nomeCampo']
        self.data = None
        self.line = None
        self.csvMode = recMap.pop('__csv__')
        
    def isEmpty(self):
        return self.data is None
     
    def toDict(self, df=True):
        return self.lineToDict(self.data, df)
    
    def lineToDict(self, r, df=True):
        ds = {}
        if r is None:
            return ds
        if df:
            r = self.applyDefault(r)
        for k in self.recMap:
            if k in self.exportIgnore:
                continue
            f = self.recMap[k]
            if f.get('composed'):
                for kd in self.composedToDict(f, r):
                    ds[kd] = r.get(kd)
            else:
                ds[k] = r.get(k)
        return ds
    
    def composedToDict(self, f, r):
        refKey = r.get(f['refField'])
        fields = f['set'][refKey]
        ds = {}
        for kd in fields:
            ds[kd] = r.get(kd)
        return ds
    
    def clear(self):
        self.data = None
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
        if self.csvMode:
            return self.parseCsv(line)
        
        m = self.recMap
        r = dict()
        
        for key in m:
            f = m[key]
            try:
                if f.get('composed'):
                    cf = self.parseComposedField(line, f['position'], r[f['refField']], f['set'])
                    for kd in cf:
                        r[kd] = cf[kd]
                else:
                    r[key] = self.parseField(key, f, f['range'], line)
            except ValueError as e:
                self.handleException(line, key, e)
                r[key] = None
        self.data = r
        self.line = line
        return r
    
    def parseCsv(self, line):
        m = self.recMap
        r = dict()
        fieldOrder = sorted(m.items(), key = lambda kv: kv[1]['range'][0])
        fieldSorted = [kv[0] for kv in fieldOrder]
        values = line.strip().split(';')
        
        for i,key in enumerate(fieldSorted):
            f = m[key]
            try:
                if f.get('composed'):
                    raise Exception('Cannot handle composed csv record')
                else:
                    r[key] = self.parseValue(key, f, values[i], line)
            except ValueError as e:
                self.handleException(line, key, e)
                r[key] = None
        self.data = r
        self.line = line
        return r
    
    def parseComposedField(self, line, pos, refKey, fSet):
        if refKey not in fSet:
            self.handleException(line, refKey, ValueError('No field set defined for key: {:s}'.format(refKey)))
        fields = fSet[refKey]
        r = {}
        for fd in fields:
            k = fd['name']
            rd = [pos, pos + fd['size'] - 1]
            r[k] = self.parseField(k, fd, rd, line)
            pos = pos + fd['size']
        return r
    
    def parseField(self, k, f, r, line):
        v = line[r[0]-1:r[1]]
        return self.parseValue(k, f, v, line)
    
    def parseValue(self, k, f, v, line):
        t = f['type']
        v = v.strip()
        
        if self.isBlankField(v):
            return None
        
        if 'special' in f:
            s = self.readSpecial(f, v)
            if s is not None:
                return s
        
        value = parseDataType(v, t)
        try:
            validateDataType(value, t)
            if 'validate' in f:
                self.validateField(f['validate'], value)
        except ValidationException as e:
            self.handleException(line, k, e)
            return value
            
        return value
    
    def validateField(self, validate, v):
        if v is None:
            return

        if 'range' in validate:
            r = validate['range']
            if v < r[0] or v > r[1]:
                raise ValidationException('range', v, r, 'between')

        if 'value' in validate:
            if v != validate['value']:
                raise ValidationException('value', v, validate['value'], '=')
            
        if 'list' in validate:
            if v not in validate['list']:
                raise ValidationException('list', v, validate['list'], 'in')
            
        if 'min' in validate:
            if v < validate['min']:
                raise ValidationException('min', v, validate['min'], '>=')
            
    def readSpecial(self, f, value):
        sList = f['special']
        for s in sList:
            if value.strip() == s:
                return s
        return None
    
    def handleException(self, line, field, ex):
        logger = logging.getLogger(__name__)
        logger.warning('Parse exception: %s \nField: %s \nLine: %s', str(ex), field, line.strip())
    