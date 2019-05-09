'''
Created on 23 de jul de 2018

@author: Renan
'''
from deckparser.importers.dessem.core.dataType import parseDataType
from deckparser.importers.dessem.core.record import record
from deckparser.importers.dessem.core.table import table
import xml.etree.ElementTree as ET
import os

class xmlReader:
    def __init__(self, configPath):
        self.configPath = configPath
    
    def decodeDsFile(self, df, fileName):
        fullPath = os.path.join(self.configPath, fileName)
        tree = ET.parse(fullPath)
        rootNode = tree.getroot()
        
        #name = rootNode.attrib['name']
        for child in rootNode:
            name, rec = self.decodeRec(child)
            if child.tag == 'record':
                df.addRec(name, record(rec))
            elif child.tag == 'table':
                df.addTable(name, table(rec))
        
    def decodeRec(self, node):
        rec = dict()
        name = node.attrib['name']
        
        for child in node:
            if child.tag == 'field':
                try:
                    nf, field = self.decodeField(child)
                except KeyError:
                    print('Error reading field "{:s}" in record "{:s}"'.format(child.attrib['name'], name))
                    raise
                rec[nf] = field
        return name, rec
        
    def decodeField(self, node, cpsField=False):
        f = dict()
        att = node.attrib
        name = att['name']
        
        if 'special' in att:
            f['special'] = self.decodeList(att['special'], None)
        
        if 'composed' in att and att['composed'] == 'True':
            f['composed'] = True
            f['position'] = int(att['position'])
            f['refField'] = att['refField']
            caseSet = dict()
            for setNode in node.iter('set'):
                for caseNode in setNode:
                    val = caseNode.attrib['value']
                    caseSet[val] = dict()
                    for fdNode in caseNode:
                        nd, fd = self.decodeField(fdNode, cpsField=True)
                        caseSet[val][nd] = fd
            f['set'] = caseSet
        else:
            f['type'] = att['type']
            if 'default' in att:
                f['default'] = parseDataType(att['default'], f['type'])
            
            if cpsField:
                f['size'] = int(att['size'])
            else:
                c = att['c']
                if 'cf' in att:
                    cf = att['cf']
                    f['range'] = [int(c), int(cf)]
                else:
                    f['range'] = [int(c), int(c)]
        
        for child in node:
            if child.tag == 'validate':
                f['validate'] = self.decodeValidation(child, f['type'])
        
        return name, f
    
    def decodeList(self, v, t):
        if v.find(';') < 0:
            return [v]
        sList = v.split(';')
        vList = []
        for s in sList:
            vList.append(parseDataType(s, t))
        return vList
        
    def decodeValidation(self, node, vType):
        f = dict()
        att = node.attrib
        if 'value' in att:
            f['value'] = parseDataType(att['value'], vType)
        if 'range' in att:
            f['range'] = self.decodeList(att['range'], vType)
        if 'list' in att:
            f['list'] = self.decodeList(att['list'], vType)
        if 'min' in att:
            f['min'] = parseDataType(att['min'], vType)
        return f
        