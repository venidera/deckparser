from logging import info,debug

from deckparser.decompzipped import DecompZipped
#from deckparser.decompdicted import DecompDicted

from deckparser.importers.newave.importHIDR import importHIDR
from deckparser.importers.decomp.importDADGER import importDADGER
from deckparser.importers.decomp.importVAZOES import importVAZOES
from deckparser.importers.decomp.importRELATO import importRELATO

def decomp2dicts(fn,sem: int = None,reg = None):
    """
    Open the zipped file and start to import data into python dicts and lists
    """
    dz = DecompZipped(fn=fn)
    if dz.zipLoaded():

        if sem==None:
            dd = []
            for i in range(1,dz.numSemanas()+1):
                HIDR, HIDRcount = importHIDR(fn=dz.extractFile(i,'HIDR'))
                dd.append({
                    "DADGER": importDADGER(dz.openFileExtData(i,'DADGER')),
                    "VAZOES": importVAZOES(fn=dz.extractFile(i,'VAZOES'),blockSize=HIDRcount),
                    "RELATO": importRELATO(dz.openFileExtData(i,'RELATO'))
                })
            return dd
        else:
            if reg==None:
                if sem >= 1 and sem <= dz.numSemanas():
                    HIDR, HIDRcount = importHIDR(fn=dz.extractFile(sem,'HIDR'))
                    return {
                        "DADGER": importDADGER(dz.openFileExtData(sem,'DADGER')),
                        "VAZOES": importVAZOES(fn=dz.extractFile(sem,'VAZOES'),
                                               blockSize=HIDRcount),
                        "RELATO": importRELATO(dz.openFileExtData(sem,'RELATO'))

                    }
                raise ValueError("Semana inválida")
            elif reg=="VAZOES":
                HIDR, HIDRcount = importHIDR(fn=dz.extractFile(sem,'HIDR'))
                return importVAZOES(fn=dz.extractFile(sem,'VAZOES'),
                                    blockSize=HIDRcount)
            elif reg=='RELATO':
                return importRELATO(dz.openFileExtData(sem,'RELATO'))
            else:
                return importDADGER(dz.openFileExtData(sem,'DADGER'),reg)
            
    else:
        return None
