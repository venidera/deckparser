from logging import info,debug

from deckparser.decompzipped import DecompZipped
#from deckparser.decompdicted import DecompDicted

from deckparser.importers.newave.importHIDR import importHIDR
from deckparser.importers.decomp.importDADGER import importDADGER
from deckparser.importers.decomp.importDADGNL import importDADGNL
from deckparser.importers.decomp.importVAZOES import importVAZOES
from deckparser.importers.decomp.importRELATO import importRELATO

def decomp2dicts(fn,r_fn = None, sem: int = None,reg = None):
    """
    Open the zipped file and start to import data into python dicts and lists
    """
    dz = DecompZipped(fn=fn,r_fn=r_fn)
    if dz.zipLoaded():

        if sem==None:
            dd = []
            for i in range(1,dz.numSemanas()+1):
                HIDR, HIDRcount = importHIDR(fn=dz.extractFile(i,'HIDR'))
                try:
                    r_f = dz.openFileExtData(i,'RELATO')
                except:
                    r_f = None

                if r_f:
                    relato = importRELATO(r_f)
                else:
                    relato = None

                dd.append({
                    "CASO": dz.openFileExtData(i,'CASO')[0].strip().upper(),
                    "DADGER": importDADGER(dz.openFileExtData(i,'DADGER')),
                    "DADGNL": importDADGNL(dz.openFileExtData(i,'DADGNL')),
                    "VAZOES": importVAZOES(fn=dz.extractFile(i,'VAZOES'),blockSize=HIDRcount),
                    "RELATO": relato
                })
            return dd
        else:
            if reg==None:
                if sem >= 1 and sem <= dz.numSemanas():
                    HIDR, HIDRcount = importHIDR(fn=dz.extractFile(sem,'HIDR'))
                    try:
                        r_f = dz.openFileExtData(sem,'RELATO')
                    except:
                        r_f = None

                    if r_f:
                        relato = importRELATO(r_f)
                    else:
                        relato = None

                    return {
                        "CASO": dz.openFileExtData(sem,'CASO')[0].strip().upper(),
                        "DADGER": importDADGER(dz.openFileExtData(sem,'DADGER')),
                        "DADGNL": importDADGNL(dz.openFileExtData(sem,'DADGNL')),
                        "VAZOES": importVAZOES(fn=dz.extractFile(sem,'VAZOES'),
                                               blockSize=HIDRcount),
                        "RELATO": relato

                    }
                raise ValueError("Semana inválida")
            elif reg=="VAZOES":
                HIDR, HIDRcount = importHIDR(fn=dz.extractFile(sem,'HIDR'))
                return importVAZOES(fn=dz.extractFile(sem,'VAZOES'),
                                    blockSize=HIDRcount)
            elif reg=='RELATO':
                return importRELATO(dz.openFileExtData(sem,'RELATO'))
            elif reg in ('TG','GS','NL','GL'):
                return importDADGNL(dz.openFileExtData(sem,'DADGNL'),reg)
            else:
                return importDADGER(dz.openFileExtData(sem,'DADGER'),reg)

    else:
        return None
