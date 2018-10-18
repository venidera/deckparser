from deckparser.decompzipped import DecompZipped
from deckparser.decompdicted import DecompDicted

from deckparser.importers.decomp.importDADGER import importDADGER

from pprint import pprint

def decomp2dicts(fn,reg=None):
    """
    Open the zipped file and start to import data into python dicts and lists
    """
    dz = DecompZipped(fn=fn)
    if dz.zipLoaded():
        dd = DecompDicted()
        dd.DADGER = importDADGER(dz.openFileExtData(1,'DADGER'),reg)

        #dz.closeSemana(1)
        #dd = DecompDicted()
        #dd.dirname = dz.dirname
        #dd.filename = dz.filename
        #dd.fhash = dz.fhash

        #dd.DGER = importDGER(dz.openFile(fnp='dger'))
        #dd.SISTEMA = importSISTEMA(dz.openFileExtData(fnp='sistema'),dd.DGER)
        #dd.process_ss()
        if reg!= None and reg!="VAZOES":
            return dd.DADGER
        else:
            return dd
    else:
        return None
