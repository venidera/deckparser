'''
Created on 9 de nov de 2018

@author: Renan Maciel
'''

class ValidationException(Exception):
    def __init__(self, vType, value, valid, condition):
        self.type = vType
        self.value = value
        self.valid = valid
        self.condition = condition
    
    def __str__(self):
        return 'Validation exception (type: {:s}, value = {:s}, valid: {:s} {:s})'.format(
            self.type, str(self.value), str(self.condition), str(self.valid))
    