'''
Created on 4 de jul de 2018

@author: Renan
'''

from datetime import date
from deckparser.dessem2dicts import dessem2dicts
from deckparser.importers.dessem.util import printDict

fn = '<Caminho para o arquivo compactado que contem os decks>'
dias = [date(2018,5,25)]
r = False
dc = dessem2dicts(fn, dias, r)
for d in dias:
    printDict(dc[d][r]['entdados']['UH'], 0)

'''
dirDS = <Caminho para o diretorio que contem o deck>

from deckparser.importers.dessem.util import showHeader
showHeader('entdados')

from deckparser.importers.dessem.util import dsFileTest
dsFileTest(dirDS, 'entdados')

from deckparser.importers.dessem.util import listCases, showHeader
for cs in listCases():
    showHeader(cs)

from deckparser.importers.dessem.util import listCases, dsFileTest
for cs in listCases():
    dsFileTest(dirDS, cs)

from deckparser.importers.dessem.util import fieldSearch
fieldSearch(reField='.*')
'''