import re
from logging import info,debug
 
def importRELATO(data):
    # definicoes
    ws = '\s+'
    estagioExp = '([0-9])'
    floatExp = '([-+]?[0-9]*\.?[0-9]*)'
    linhaTabela = ws+'[X\-]+'+ws

    def parseQnat(val):
        val = val.split('(')
        try:
            val[0] = float(val[0].strip())
        except:
            val[0] = val[0].strip()
        try:
            val[1] = float(val[1][:-1].strip())
        except:
            val[1] = val[1][:-1].strip()
        
        return {
            'value': val[0],
            'pMLT': val[1]
        }
    
    def parsePerdHidr(val):
        val = val.split(' ')
        
        return {
            'valor': float(val[0]),
            'unidade': val[1]
        }        
    
    tableRefs = {
        'REL_DADOS_CAD_HIDR': {
            'hexp': [ws+'Relatorio'+ws+'dos'+ws+'Dados'+ws+'do'+ws+'Cadastro'+ws+'.+'+ws+'do'+ws+'estagio:'+ws+estagioExp+ws+'\(ALTCAD\)'],
            'eline': 0,
            'hlines': 5,
            'rows': [ { 'name': 'Num', 'parser': int },
                      { 'name': 'Nome'},
                      { 'name': 'Ssis'},
                      { 'name': 'PosVaz', 'parser': int },
                      { 'name': 'UsiJusOpe', 'parser': int },
                      { 'name': 'UsiDesOpe', 'parser': int },
                      { 'name': 'UsiJusEne', 'parser': int },
                      { 'name': 'VolumeMaximo', 'parser': float },
                      { 'name': 'VolumeMinimo', 'parser': float },
                      { 'name': 'VutilInic', 'parser': float },
                      { 'name': 'PrevisOper' },
                      { 'name': 'Pinst', 'parser': float },
                      { 'name': 'PerdasHid', 'parser': parsePerdHidr },
                      { 'name': 'QturMaxima', 'parser': float },
                      { 'name': 'QdefMinima', 'parser': float },
                      { 'name': 'VertMaximo', 'parser': float },
                      { 'name': 'ProdutEqv', 'parser': float },
                      { 'name': 'SomprdEqv', 'parser': float },
                      { 'name': 'Produt65VU', 'parser': float },
                      { 'name': 'Somprd65VU', 'parser': float },
                      { 'name': 'TIP'} ],
            'type': 'x_delimited'
        },        
        'REL_OP_HIDR': {
            'hexp': ['RELATORIO'+ws+'DA'+ws+'OPERACAO',
                     ws,
                     '.+'+ws+'\/'+ws+'SEMANA'+ws+'[0-9]'+ws+'\-'+ws+'ESTAGIO'+ws+estagioExp+ws+'\/'+ws+'.*',
                     ws,
                     re.escape('# Aproveitamento(s) com evaporacao'),
                     re.escape('* Aproveitamento(s) com tempo de viagem da afluencia'),
                     re.escape('@ Aproveitamento(s) com cota abaixo da crista do vert.'),
                     re.escape('$ Aproveitamento(s) de cabeceira : def.minima = zero'),
                     linhaTabela,
                     'No.'+ws+'Usina'+ws+'Volume'+ws+'\(\% V\.U\.\)'+ws+'Vazoes'+ws+'\(M3\/S\)'+ws+'Energia'+ws+'\(MWmed\)'+ws+'\-'+ws+'CGC'+ws+'Pdisp'],
            'eline': 2,
            'hlines': 11,
            'rows': [ { 'name': 'No', 'parser': int },
                      { 'name': 'Usina', 'parser': lambda val: val[:-5].strip() },
                      { 'name': 'VolIni', 'parser': float },
                      { 'name': 'VolFin', 'parser': float },
                      { 'name': 'VolEsp', 'parser': float },
                      { 'name': 'Qnat', 'parser': parseQnat },
                      { 'name': 'Qafl', 'parser': float },
                      { 'name': 'Qdef', 'parser': float },
                      { 'name': 'GER_1', 'parser': float },
                      { 'name': 'GER_2', 'parser': float },
                      { 'name': 'GER_3', 'parser': float },
                      { 'name': 'Media', 'parser': float },
                      { 'name': 'VT', 'parser': float },
                      { 'name': 'VNT', 'parser': float },
                      { 'name': 'Ponta', 'parser': float },
                      { 'name': 'FPCGC', 'parser': float } ],
            'type': 'x_delimited'
        },
        'REL_BAL_HIDR': {
            'hexp': ['RELATORIO'+ws+'DO'+ws+'BALANCO'+ws+'HIDRAULICO',
                     ws,
                     '.+'+ws+'\/'+ws+'SEMANA'+ws+'[0-9]'+ws+'\-'+ws+'ESTAGIO'+ws+estagioExp+ws+'\/'+ws+'.*',
                     ws,
                     linhaTabela,
                     'Usina'+ws+'Qinc'+ws+'Qafl'+ws+'Qtur'+ws+'Qver'+ws+'Qdes'+ws+'Qirr\+Qbb'+ws+'Qda'+ws+'Qret'+ws+'Qevp'+ws+'Qarm'+ws+'Montante'+ws+'Qdef'+ws+'Qdes'+ws+'Lag'+ws+'Fator'],
            'eline': 2,
            'hlines': 7,
            'rows': [ { 'name': 'Usina' },
                      { 'name': 'Qinc', 'parser': float },
                      { 'name': 'Qafl', 'parser': float },
                      { 'name': 'Qtur', 'parser': float },
                      { 'name': 'Qver', 'parser': float },
                      { 'name': 'Qdes', 'parser': float },
                      { 'name': 'Qirr+Qbb', 'parser': float },
                      { 'name': 'Qda', 'parser': float },
                      { 'name': 'Qret', 'parser': float },
                      { 'name': 'Qevp', 'parser': float },
                      { 'name': 'Qarm', 'parser': float },
                      { 'name': 'Montante', 'parser': float },
                      { 'name': 'Qdef', 'parser': float },
                      { 'name': 'Qdes', 'parser': float },
                      { 'name': 'Lag Fator', 'parser': float }],
            'type': 'x_delimited'
        },
        'REL_BAL_ENER': {
            'hexp': ['RELATORIO'+ws+'DO'+ws+'BALANCO'+ws+'ENERGETICO',
                     ws,
                     '.+'+ws+'\/'+ws+'SEMANA'+ws+'[0-9]'+ws+'\-'+ws+'ESTAGIO'+ws+estagioExp+ws+'\/'+ws+'.*'],
            'eline': 2,
            'hlines': 3,
            'type': 'bal_ener'
        },
        'REL_OPERACAO': {
            'hexp': ['RELATORIO'+ws+'DA'+ws+'OPERACAO',
                     ws,
                     '.+'+ws+'\/'+ws+'SEMANA'+ws+'[0-9]'+ws+'\-'+ws+'ESTAGIO'+ws+estagioExp+ws+'\/'+ws+'.*',
                     ws,
                     ws,
                     'Valor'+ws+'esperado'+ws+'do'+ws+'custo'+ws+'futuro'+'.*'],
            'eline': 2,
            'hlines': 22,
            'type': 'rel_oper'
        },
        'FLUXO_NOS_INTERCAMBIOS': {
            'hexp': ['FLUXO'+ws+'NOS'+ws+'INTERCAMBIOS'+ws+'.*'],
            'hlines': 0,
            'type': 'fluxo_int'
        }
    }


    currTable = None
    currLimits = None
    estagio = None
    row = None
    l = 0
    relato = dict()
    while l < len(data):
        # procura por tabela a ser importada
        if currTable == None:
            for tableId in tableRefs:
                table = tableRefs[tableId]
                found = True
                for eId in range(len(table['hexp'])):
                    if l+eId<len(data):
                        search = re.search(table['hexp'][eId],data[l+eId])
                    else:
                        search = False
                    if not search:
                        found = False
                        break
                    if search and 'eline' in table and eId==table['eline']:
                        estagio = int(search.group(1))
                if found:
                    currTable = tableId
                    
                    # pula linhas da definição
                    l += table['hlines']
                    
                    if table['type']=='x_delimited':
                        currLimits = data[l].split('X')
                    break
            l += 1
            continue
                
        # currTable != None
        # já encontrou tabela, importa linhas
        
        # verifica e ajusta estrutura de retorno (relato)
        table = tableRefs[currTable]
        if 'eline' in table:
            if currTable not in relato:
                relato[currTable] = dict()
            if estagio not in relato[currTable]:
                relato[currTable][estagio] = list()
            


        # ações de leitura conforme tipo
        if table['type']=='x_delimited':

            # verifica se é última linha da tabela
            search = re.search(linhaTabela,data[l])
            if search:
                currTable = None
                currLimits = None
                l +=1
                continue

            f = 0
            ini = 0
            row = dict()
            for rowdef in table['rows']:
                ini += len(currLimits[f])+1
                fim = ini + len(currLimits[f+1])
                if 'parser' in rowdef:
                    try:
                        parser = rowdef['parser']
                        row[rowdef['name']] = parser(data[l][ini:fim])
                    except:
                        row[rowdef['name']] = data[l][ini:fim].strip()
                else:
                    row[rowdef['name']] = data[l][ini:fim].strip()
                f += 1
            relato[currTable][estagio].append(row)
            row = None
            l += 1
            continue
                    
        if table['type']=='bal_ener':
            search = re.search(ws+'Subsistema'+ws+'(SE|S|NE|N|FC)',data[l])
            if search:
                row = {
                    'Subsistema': search.group(1)
                }
                l += 1
                continue

            if row==None:
                l += 1
                continue

            
            search = re.search(ws+'EAR_ini:'+ws+floatExp+ws+'\(Mwmes\)'+
                               ws+'ENA:'+ws+floatExp+ws+'\(Mwmed\)'+
                               ws+'EAR_fim:'+ws+floatExp+ws+'\(Mwmes\)'+ws,
                               data[l], re.IGNORECASE)
            if search:
                row['EAR_ini'] = float(search.group(1))
                row['ENA'] = float(search.group(2))
                row['EAR_fim'] = float(search.group(3))
                l += 1
                continue

            exp = (ws+'Medio'+ws+floatExp+
                   ws+floatExp+ws+floatExp+
                   ws+floatExp+ws+floatExp+
                   ws+floatExp+ws+floatExp+
                   ws+floatExp+ws+floatExp+
                   ws+'(?:SE|S|NE|N|FC)\s?:'+
                   ws+floatExp+'\*')
            if row['Subsistema']=='SE':
                exp += ws+floatExp+ws+floatExp
            search = re.search(exp,data[l])
            if search:
                if row['Subsistema']=='FC':
                    currTable = None
                    l += 1
                    continue

                row['Mercado'] = float(search.group(1))
                row['Bacia'] = float(search.group(2))
                row['Cbomba'] = float(search.group(3))
                row['Ghid'] = float(search.group(4))
                row['Gter'] = float(search.group(5))
                row['GterAT'] = float(search.group(6))
                row['Deficit'] = float(search.group(7))
                row['Compra'] = float(search.group(8))
                row['Venda'] = float(search.group(9))
                row['Interligacao'] = float(search.group(10))
                if row['Subsistema']=='SE':
                    row['Itaipu50'] = float(search.group(11))
                    row['Itaipu60'] = float(search.group(12))
                relato[currTable][estagio].append(row)
                row = None
                l += 1
                continue                                                           
            l += 1
            continue
        if table['type']=='rel_oper':                
            search = re.search(ws+'Custo'+ws+'marginal'+ws+'de'+ws+'operacao'+
                               ws+'do'+ws+'subsistema'+
                               ws+'(SE|S|NE|N|FC)\s*:'+
                               ws+floatExp+ws+'.*',
                               data[l])
            if search:
                relato[currTable][estagio].append({
                    'Subsistema': search.group(1),
                    'CMO': float(search.group(2))
                })
                if search.group(1)=='FC':
                    currTable = None
            l += 1
            continue
        
        if table['type']=='fluxo_int':            
            # primeira linha da tabela, define limites dos campos
            if currLimits == None:
                currLimits = data[l].split('X')
                table['rows'] = list()
                l += 1
                continue

            # segunda linha da tabela, define nome dos campos
            if len(table['rows'])==0:
                ini = 0
                for f in range(len(currLimits)-2):
                    ini += len(currLimits[f])+1
                    fim = ini + len(currLimits[f+1])
                    field = data[l][ini:fim].strip()
                    table['rows'].append(field)
                l += 1
                continue

            # linha logo antes dos dados
            if currTable not in relato:
                relato[currTable] = list()
                l += 1
                continue

            # verifica se é ultima linha para finalizar
            search = re.search(linhaTabela,data[l])
            if search:
                currTable = None
                currLimits = None
                l += 1
                continue
                
            
            # carrega linha
            f = 0
            ini = 0
            row = dict()
            for rowname in table['rows']:
                ini += len(currLimits[f])+1
                fim = ini + len(currLimits[f+1])
                field = data[l][ini:fim].strip()
                try:
                    row[rowname] = int(field)
                except:
                    try:
                        row[rowname] = float(field)
                    except:
                        row[rowname] = field
                f += 1
            relato[currTable].append(row)
            l += 1
            continue
    return relato
