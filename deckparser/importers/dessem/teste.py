'''
Created on 4 de jul de 2018

@author: Renan
'''
dirDS = 'C:\\Users\\Renan\\Documents\\Doutorado\\P&D\\Leitura de dados\\Decks de referencia\\DES_CCEE_20180525_ComRede\\'

from deckparser.importers.dessem.util import listCases, dsFileTest
for cs in listCases():
    dsFileTest(dirDS, cs)

'''
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