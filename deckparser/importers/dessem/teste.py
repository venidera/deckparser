'''
Created on 4 de jul de 2018

@author: Renan
'''
dirDS = 'C:\\Users\\Renan\\Documents\\Doutorado\\P&D\\Leitura de dados\\Decks de referencia\\DES_CCEE_20180525_ComRede\\'

from util import listCases, dsFileTest
for cs in listCases():
    dsFileTest(dirDS, cs)

'''
from util import showHeader
showHeader('entdados')

from util import dsFileTest
dsFileTest(dirDS, 'entdados')

from util import listCases, showHeader
for cs in listCases():
    showHeader(cs)

from util import listCases, dsFileTest
for cs in listCases():
    dsFileTest(dirDS, cs)

from util import fieldSearch
fieldSearch(reField='.*')
'''