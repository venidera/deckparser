'''
Created on 23 de jul de 2018

@author: Renan
'''

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
        raise ValueError('Invalid hour')
    
def validateDay(v):
    if v < 1 or v > 31:
        raise ValueError('Invalid day')
    
def validateWeekday(v):
    if v < 1 or v > 7:
        raise ValueError('Invalid day (week)')
    
def validateMonth(v):
    if v < 1 or v > 12:
        raise ValueError('Invalid month')
    
def validateYear(v):
    if v < 1900:
        raise ValueError('Invalid year')
    
def validateBin(v):
    if v not in [0, 1]:
        raise ValueError('Invalid bin')
    