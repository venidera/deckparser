'''
Created on 23 de jul de 2018

@author: Renan
'''

def printDict(d, lvm, lv=0):
    if lv <= lvm:
        if isinstance(d, list):
            for ln in d:
                printDict(ln,lvm,lv+1)
        elif isinstance(d, dict):
            for k in d:
                print('\t'*lv+str(k))
                printDict(d[k],lvm,lv+1)
        else:
            print('\t'*lv+str(d))
    else:
        print('\t'*lv+str(d))
