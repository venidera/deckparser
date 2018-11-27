'''
Created on 4 de jul de 2018

@author: Renan
'''

from datetime import date
from deckparser.dessem2dicts import dessem2dicts
from deckparser.importers.dessem.util import printDict

fn = 'C:\\Users\\Renan\\Documents\\Doutorado\\P&D\\Leitura de dados\\Decks de referencia\\des_201810.zip'
dias = []
for d in range(1,31):
    dias.append(date(2018,5,d))

rd = [True, False]
dc = dessem2dicts(fn, dias, rd)
for d in dc:
    for r in dc[d]:
        printDict(dc[d][r]['entdados']['UH'], 0)

'''
from deckparser.importers.dessem.loader import Loader

dirDS = 'C:\\Users\\Renan\\Documents\\Doutorado\\P&D\\Leitura de dados\\Decks de referencia\\DES_CCEE_20180525_ComRede\\'

ld = Loader(dirDS)
ld.loadElet([99])
'''
