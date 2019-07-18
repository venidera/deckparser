from deckparser.suishizipped import SuishiZipped
# from deckparser.suishidicted import SuishiDicted
from deckparser.importers.suishi.loader import Loader
# from deckparser.importers.newave.importDGER import importDGER
# from deckparser.importers.newave.importSISTEMA import importSISTEMA
# from deckparser.importers.newave.importCAR import importCAR
# from deckparser.importers.newave.importTERM import importTERM
# from deckparser.importers.newave.importEXPT import importEXPT
# from deckparser.importers.newave.importCONFT import importCONFT
# from deckparser.importers.newave.importCLAST import importCLAST
# from deckparser.importers.newave.importMANUTT import importMANUTT
# from deckparser.importers.newave.importHIDR import importHIDR
# from deckparser.importers.newave.importCONFHD import importCONFHD
# from deckparser.importers.newave.importMODIF import importMODIF
# from deckparser.importers.newave.importDSVAGUA import importDSVAGUA
# from deckparser.importers.newave.importVAZOES import importVAZOES
# from deckparser.importers.newave.importCADIC import importCADIC
# from deckparser.importers.newave.importEXPH import importEXPH
# from deckparser.importers.newave.importPATAMAR import importPATAMAR
# from deckparser.importers.newave.importCADTERM import importCADTERM
# from deckparser.importers.newave.importSHIST import importSHIST
# from deckparser.importers.newave.importREE import importREE
# from logging import info


def suishi2dicts(fn):
    """
    Open the zipped file and start to import data into python dicts and lists
    """
    dz = SuishiZipped(fn=fn)
    if dz.zipLoaded():
        loader = Loader(dz)
        return loader.dd
    else:
        return None
