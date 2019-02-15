from deckparser.importers.dessem.out.pdo_base import pdo_base, TableDef

class pdo_sist(pdo_base):
    def __init__(self):
        super().__init__()
    
    def getTableKey(self):
        return 'pdo_sist'
    
    def getTableDef(self):
        return TableDef(['intervalo', 'patamar', 'subSistema', 'cmo', 'demanda', 'perdas', 'gerPeq', 'gerFixBar', 
                         'gerHidrTot', 'gerTermTot', 'consumoBomb', 'importacao', 'exportacao', 'deficit', 
                         'saldo', 'recebimento', 'gerTermMinTot', 'gerTermMaxTot', 'earm'],
                         ['i','s','s','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f','f'],
                        [None, None, None, '$/MWH', 'MW', 'MW', 'MW', 'MW', 'MW', 'MW', 
                         'MW', 'MW', 'MW', 'MW', 'MW', 'MW', 'MW', 'MW', 'MWH'])
    