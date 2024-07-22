from deckparser.newavezipped import NewaveZipped
from deckparser.newavedicted import NewaveDicted
from deckparser.importers.newave.importDGER import importDGER
from deckparser.importers.newave.importSISTEMA import importSISTEMA
from deckparser.importers.newave.importCAR import importCAR
from deckparser.importers.newave.importTERM import importTERM
from deckparser.importers.newave.importEXPT import importEXPT
from deckparser.importers.newave.importCONFT import importCONFT
from deckparser.importers.newave.importCLAST import importCLAST
from deckparser.importers.newave.importMANUTT import importMANUTT
from deckparser.importers.newave.importHIDR import importHIDR
from deckparser.importers.newave.importCONFHD import importCONFHD
from deckparser.importers.newave.importMODIF import importMODIF
from deckparser.importers.newave.importDSVAGUA import importDSVAGUA
from deckparser.importers.newave.importVAZOES import importVAZOES
from deckparser.importers.newave.importCADIC import importCADIC
from deckparser.importers.newave.importEXPH import importEXPH
from deckparser.importers.newave.importPATAMAR import importPATAMAR
from deckparser.importers.newave.importCADTERM import importCADTERM
from deckparser.importers.newave.importSHIST import importSHIST
from deckparser.importers.newave.importREE import importREE
from logging import info


def newave2dicts(fn):
    """
    Open the zipped file and start to import data into python dicts and lists
    """
    dz = NewaveZipped(fn=fn)
    if dz.zipLoaded():
        dd = NewaveDicted()
        dd.dirname = dz.dirname
        dd.filename = dz.filename
        dd.fhash = dz.fhash
        dd.DGER = importDGER(dz.openFile(fnp='dger'))
        dd.SISTEMA = importSISTEMA(dz.openFileExtData(fnp='sistema'), dd.DGER)
        dd.process_ss()
        dd.PATDURA, dd.PATCARGA, dd.PATINTER, dd.PATNSIM, dd.np = \
            importPATAMAR(dz.openFileExtData(fnp='patamar'), dd.DGER, dd.sss)
        dd.CAR = importCAR(dz.openFileExtData(fnp='curva'), dd.DGER)
        dd.CADIC = importCADIC(dz.openFileExtData(fnp='c_adic'), dd.DGER)
        dd.TERM = importTERM(dz.openFile(fnp='term'))
        dd.CADTERM = importCADTERM(dz.openFile(fnp='cadterm'))
        dd.EXPT = importEXPT(fobj=dz.openFile(fnp='expt'), utes=dd.TERM.keys())
        dd.CONFT = importCONFT(dz.openFile(fnp='conft'))
        dd.CLAST, dd.MODIFCLAST = importCLAST(
            fobj=dz.openFile(fnp='clast'), utes=dd.TERM.keys(),
            nyears=len(dd.DGER['yph']))
        dd.MANUTT = importMANUTT(
            fobj=dz.openFile(fnp='manutt'), utes=dd.TERM.keys())
        dd.HIDR, dd.HIDRcount = importHIDR(fn=dz.extractFile(fnp='hidr'))
        for conff in ['confhd', 'confh']:
            try:
                dd.CONFHD = importCONFHD(dz.openFile(fnp=conff))
            except Exception as e:
                info('File {} not found. {}'.format(conff, e))
        for modiff in ['modif', 'modif55']:
            try:
                fobj = dz.openFile(fnp=modiff)
                if fobj:
                    dd.MODIF = importMODIF(fobj=fobj)
            except Exception as e:
                info('File {} not found. {}'.format(modiff, e))
        if 'DECK DO PMO' in dz.fns_set:
            decktype = 'pmo'
        else:
            decktype = False
        dd.DSVAGUA = importDSVAGUA(
            dz.openFileExtData(fnp='dsvagua'), uhes=dd.CONFHD.keys(),
            dger=dd.DGER, decktype=decktype)
        dd.VAZOES, dd.VAZcount, dd.vaz = importVAZOES(
            fn=dz.extractFile(fnp='vazoes'), hcount=dd.HIDRcount,
            dger=dd.DGER)
        dd.ENCHVM, dd.MOTORI = importEXPH(dz.openFileExtData(fnp='exph'))
        dd.SHISTANO = importSHIST(dz.openFileExtData(fnp='shist'))
        try:
            dd.REE, dd.REElabels = importREE(fobj=dz.openFile(fnp='ree'))
        except Exception as e:
            info('File REE.dat not found. {}'.format(e))

        # Start parse and processing data
        # Split data into data structs considering the configuration
        # for the planning study
        # dd.prepareDataStructs()
        # Apply MODIF - parse updating info and apply into structures created
        # in the last method
        # dd.processMODIF()
        # Create time series for certain values
        # dd.preparePosMODIFDataStructs()
        # Aplicar EXPH
        # dd.processEXPH()
        # Process Thermal Series
        # dd.processThermalPlants()
        # Process inflows
        # dd.loadVAZData()

        return dd
    else:
        return None
