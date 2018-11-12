'''
Created on 4 de jul de 2018

@author: Renan
'''

from datetime import date
from deckparser.dessem2dicts import dessem2dicts
from deckparser.importers.dessem.util import printDict

fn = '<Caminho para o arquivo compactado que contem os decks>'
dias = []
for d in range(1,31):
    dias.append(date(2018,5,d))

rd = [True, False]
dc = dessem2dicts(fn, dias, rd, {'filename_pattern':2})
for d in dc:
    for r in dc[d]:
        printDict(dc[d][r]['entdados']['UH'], 0)

'''
from deckparser.importers.dessem.loader import Loader

dirDS = <Caminho para o diretorio que contem o deck>

ld = Loader(dirDS)
ld.loadElet([99])
'''
