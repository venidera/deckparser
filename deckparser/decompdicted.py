#from uhe import UHE
##from ute import UTE
#from extdata import loadCodANEEL,loadPMinRest,loadRendGer
#from imputils import getUpdateIndexes
#import datetime, calendar
#import networkx as nx
from logging import info

# Chaves do MODIF: Processada?
# VOLMIN   : ok
# VOLMAX   : ok
# VAZMIN   : ok
# NUMCNJ   : ok
# NUMMAQ   : ok
# POTEFE   : ok
# PRODESP  : ok
# TEIF     : ok
# IP       : ok
# PERDHIDR : ok
# COEFEVAP : ok
# COTAAREA : ok
# VOLCOTA  : ok
# CFUGA    : ok
# VMAXT    : ok
# VMINT    : ok
# NUMBAS   : ok
# VMINP    : nao tratado
# VAZMINT  : ok

class DecompDicted(object):
    def __init__(self):
        self.DADGER = None
        self.VAZOES = None

