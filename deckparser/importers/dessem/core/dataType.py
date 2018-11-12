'''
Created on 23 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.exceptions import ValidationException

def parseDataType(v, t):
    if t == 'int' or t in ['h', 'd', 'ds', 'm', 'a', 'bin']:
        return int(v)
    if t == 'real':
        return float(v)
    return v

def validateDataType(v, t):
    if t == 'h':
        validateHour(v)
    if t == 'd':
        validateDay(v)
    if t == 'ds':
        validateWeekday(v)
    if t == 'm':
        validateMonth(v)
    if t == 'a':
        validateYear(v)
    if t == 'bin':
        validateBin(v)

def validateHour(v):
    if v < 0 or v > 24:
        raise ValidationException('hour', v, [0,24], 'between')
    
def validateDay(v):
    if v < 1 or v > 31:
        raise ValidationException('day', v, [1,31], 'between')
    
def validateWeekday(v):
    if v < 1 or v > 7:
        raise ValidationException('weeak day', v, [1,7], 'between')
    
def validateMonth(v):
    if v < 1 or v > 12:
        raise ValidationException('month', v, [1,12], 'between')
    
def validateYear(v):
    if v < 1:
        raise ValidationException('year', v, [1], '>')
    
def validateBin(v):
    if v not in [0, 1]:
        raise ValidationException('bin', v, [0,1], 'in')
    