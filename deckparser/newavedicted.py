from logging import info

# Chaves do MODIF Processadas:
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

class NewaveDicted(object):
    def __init__(self):
        # Dados de sistema e problema
        self.DGER = None
        self.SISTEMA = None
        self.CAR = None
        self.CADIC = None
        self.PATDURA = None
        self.PATCARGA = None
        self.PATINTER = None

        # Dados do parque termelétrico
        self.TERM = None
        self.CONFT = None
        self.CADTERM = None
        self.EXPT = None
        self.CLAST = None
        self.MODIFCLAST = None
        self.MANUTT = None

        # Dados do parque hidrelétrico
        self.CONFHD = None
        self.HIDR = None
        self.HIDRcount = None
        self.MODIF = None
        self.DSVAGUA = None
        self.VAZOES = None

        self.VAZcount = None
        self.VAZMAX = None

        self.ENCHVM = None
        self.MOTORI = None

        self.REE = None
        self.REElabels = None

        # Helpers
        self.nss = None
        self.sss = None
        self.ssname = None
        self.ssfict = None

    # def nu(self):
    #     if self.uh:
    #         return len(self.uh)
    #     else:
    #         return 0
    #
    # def nt(self):
    #     if self.ut:
    #         return (len(self.ut))
    #     else:
    #         return 0
    #
    # def niv(self):
    #     if self.VAZOES:
    #         anos = self.VAZOES[self.VAZOES.keys()[0]]
    #         niv = 0
    #         for ano,vaz in anos.iteritems():
    #             if ano != self.yi():
    #                 niv += 12
    #             else:
    #                 niv += self.mi() -1
    #         return niv
    #     else:
    #         return 0
    #
    # def ni(self):
    #     if self.DGER:
    #         return self.DGER['ni']
    #     else:
    #         return 0
    #
    # def mi(self):
    #     if self.DGER:
    #         return self.DGER['mi']
    #     else:
    #         return 0
    #
    # def yi(self):
    #     if self.DGER:
    #         return self.DGER['yi']
    #     else:
    #         return 0
    #
    # def txdesc(self):
    #     if self.DGER:
    #         return self.DGER['txdesc']
    #     else:
    #         return 0
    #
    def process_ss(self):
        if self.nss:
            return self.nss
        else:
            if self.SISTEMA:
                sss = list()
                ssfict = list()
                for ss in self.SISTEMA['sss'].keys():
                    if self.SISTEMA['sss'][ss]['fict'] == 0:
                        sss.append(int(ss))
                    else:
                        ssfict.append(int(ss))
                self.nss = len(sss)
                sss.sort()
                ssfict.sort()
                self.sss = list(map(str, sss))
                self.ssfict = list(map(str, ssfict))
                self.ssname = list()
                for idss in self.sss:
                    self.ssname.append(self.SISTEMA['sss'][idss]['name'])
                return self.nss
            else:
                return 0
    # """
    # def uheIdxHidrCode(self,coduhe):
    # ret = 0
    # if coduhe == '0':
    #     return ret
    # for i,uh in enumerate(self.uh):
    #     if uh.hcod == coduhe:
    #     ret = i
    #     break
    # return ret
    #
    # def uheIdxEletCode(self,coduhe):
    # if coduhe == '0':
    #     return -1
    # for i,uh in enumerate(self.uh):
    #     if uh.cd == coduhe:
    #     return i
    #
    # def uteIdxTermCode(self,codute):
    # if codute == '0':
    #     return -1
    # for i,ut in enumerate(self.ut):
    #     if ut.cd == codute:
    #     return i
    #
    # def codHIDR(self,cd):
    # ret = 0
    # for k,v in self.codaneel.iteritems():
    #     if cd == v:
    #     ret = k
    #     break
    # return ret
    #
    # def rendGer(self,cd):
    # cjtg = list()
    # if cd in self.rendger.keys():
    #     for k in self.rendger[cd].keys():
    #         cjtg.append({'ncjtg':k,'rend':self.rendger[cd][k]})
    # return cjtg
    #
    # def potMinRest(self,cd):
    # potmin = list()
    # if cd in self.pminrest.keys():
    #     for k in self.pminrest[cd].keys():
    #     # fornece em MW
    #     potmin.append({'ncjtg':k,'potmin':self.pminrest[cd][k] / 1000})
    # return potmin
    # """
    #
    # def prepareDataStructs(self):
    #     # Polinomios
    #     self.POLS = dict()
    #     self.POLVOLCOTA = dict()
    #     self.POLAREACOTA = dict()
    #     self.POLCOTAVAZAO = dict()
    #     self.NARefCV = dict()
    #     # TEIF, IP e INDISP
    #     self.TEIF = dict()
    #     self.IP = dict()
    #     # VOL e VAZ(DEF)
    #     self.VOLMIN = dict()
    #     self.VOLMAX = dict()
    #     self.DEFMIN = dict()
    #     self.DEFMAX = dict()
    #     # ISFIO
    #     self.ISFIO = dict()
    #     # PRODESP
    #     self.PRODESP = dict()
    #     # PERDHIDR
    #     self.PERDHIDR = dict()
    #     # NUMBAS
    #     self.NUMBAS = dict()
    #     # NUMCNJ
    #     self.NUMCNJ = dict()
    #     # NUMMAQ e outros cd CNJ
    #     self.NUMMAQ = dict()
    #     self.POTEFE = dict()
    #     self.ENGEFE = dict()
    #     self.HEFE = dict()
    #     # CFUGA - serie
    #     self.CFUGA = dict()
    #     # VMAXT, VMINT, VAZMINT
    #     self.VMAXT = dict()
    #     self.VMINT = dict()
    #     self.VAZMINT = dict()
    #     # Coeficientes de Evaporacao
    #     self.EVAP = dict()
    #     for k,v in self.CONFHD.iteritems():
    #         ph_pol = list()
    #         qhg_pol = list()
    #         qht_pol = list()
    #         for np in range(1,6):
    #             cf_ph = list()
    #             cf_qhg = list()
    #             cf_qht = list()
    #             for ncf in range(1,6):
    #                 cf_ph.append(self.HIDR[v['nome']]['Pol_PH_'+str(np)+'_'+str(ncf)])
    #                 cf_qhg.append(self.HIDR[v['nome']]['Pol_QHG_'+str(np)+'_'+str(ncf)])
    #                 cf_qht.append(self.HIDR[v['nome']]['Pol_QHT_'+str(np)+'_'+str(ncf)])
    #             ph_pol.append(cf_ph)
    #             qhg_pol.append(cf_qhg)
    #             qht_pol.append(cf_qht)
    #         self.POLS[k] = {'ph': ph_pol, 'qhg': qhg_pol, 'qht': qht_pol}
    #         self.POLVOLCOTA[k] = [
    #             self.HIDR[v['nome']]['VolxCota_1'],
    #             self.HIDR[v['nome']]['VolxCota_2'],
    #             self.HIDR[v['nome']]['VolxCota_3'],
    #             self.HIDR[v['nome']]['VolxCota_4'],
    #             self.HIDR[v['nome']]['VolxCota_5']]
    #         self.POLAREACOTA[k] = [
    #             self.HIDR[v['nome']]['AreaxCota_1'],
    #             self.HIDR[v['nome']]['AreaxCota_2'],
    #             self.HIDR[v['nome']]['AreaxCota_3'],
    #             self.HIDR[v['nome']]['AreaxCota_4'],
    #             self.HIDR[v['nome']]['AreaxCota_5']]
    #         self.POLCOTAVAZAO[k] = list()
    #         self.NARefCV[k] = list()
    #         for npolcc in range(self.HIDR[v['nome']]['NumCurvChave']):
    #             self.POLCOTAVAZAO[k].append([
    #                 self.HIDR[v['nome']]['CurvaChave_'+str(npolcc+1)+'_1'],
    #                 self.HIDR[v['nome']]['CurvaChave_'+str(npolcc+1)+'_2'],
    #                 self.HIDR[v['nome']]['CurvaChave_'+str(npolcc+1)+'_3'],
    #                 self.HIDR[v['nome']]['CurvaChave_'+str(npolcc+1)+'_4'],
    #                 self.HIDR[v['nome']]['CurvaChave_'+str(npolcc+1)+'_5']])
    #         self.NARefCV[k].append(self.HIDR[v['nome']]['NARefCurvChave_'+str(npolcc+1)])
    #         self.TEIF[k] = self.HIDR[v['nome']]['TEIF']
    #         self.IP[k] = self.HIDR[v['nome']]['IP']
    #         self.VOLMIN[k] = self.HIDR[v['nome']]['VolMinOper']
    #         self.VOLMAX[k] = self.HIDR[v['nome']]['VolMaxOper']
    #         self.DEFMIN[k] = self.HIDR[v['nome']]['VazNatMinHist']
    #         self.DEFMAX[k] = 1e+20
    #         if self.HIDR[v['nome']]['Regulacao'].strip() == 'D':
    #             self.ISFIO[k] = 1
    #         else:
    #             self.ISFIO[k] = 0
    #         self.PRODESP[k] = self.HIDR[v['nome']]['ProdEspec']
    #         self.PERDHIDR[k] = self.HIDR[v['nome']]['CoefPerdHidr']
    #         self.NUMBAS[k] = self.HIDR[v['nome']]['NumUnidBase']
    #         self.NUMCNJ[k] = self.HIDR[v['nome']]['NumConjMaq']
    #         self.NUMMAQ[k] = dict()
    #         self.POTEFE[k] = dict()
    #         self.ENGEFE[k] = dict()
    #         self.HEFE[k] = dict()
    #         for ncj in range(self.NUMCNJ[k]):
    #             self.NUMMAQ[k][ncj] = self.HIDR[v['nome']]['NumMaqConj_'+str(ncj+1)]
    #             self.POTEFE[k][ncj] = self.HIDR[v['nome']]['PotEfetConj_'+str(ncj+1)]
    #             self.ENGEFE[k][ncj] = self.HIDR[v['nome']]['EngEfetConj_'+str(ncj+1)]
    #             self.HEFE[k][ncj] = self.HIDR[v['nome']]['HNomConj_'+str(ncj+1)]
    #         self.CFUGA[k] = [ self.HIDR[v['nome']]['CFugaMed'] for x in range(self.ni()) ]
    #         if v['uexis'] == 'NE':
    #             self.VMINT[k] = [ 0.0 for x in range(self.ni()) ]
    #             self.VMAXT[k] = [ 0.0 for x in range(self.ni()) ]
    #         else:
    #             if self.ISFIO[k] == 1:
    #                 # FIO DAGUA = Reservatorio nao varia, com minimo e maximo iguais ao VOLMAX
    #                 self.VMINT[k] = [ self.VOLMAX[k] for x in range(self.ni()) ]
    #             else:
    #                 # Reservatorio varia
    #                 self.VMINT[k] = [ self.VOLMIN[k] for x in range(self.ni()) ]
    #         self.VMAXT[k] = [ self.VOLMAX[k] for x in range(self.ni()) ]
    #         self.VAZMINT[k] = [ self.DEFMIN[k] for x in range(self.ni()) ]
    #         self.EVAP[k] = list()
    #         for midx in range(1,13):
    #             self.EVAP[k].append(float(self.HIDR[v['nome']]['CoefEvap_'+str(midx)]))
    #     # Thermal structures
    #     self.FCMAX = None
    #     self.IPTER = None
    #     self.TEIFT = None
    #     self.GTMIN = None
    #     self.tPOT = None
    #     self.tPOTINST = None
    #     self.COMB = None
    #     self.CUST = None
    #     self.TUG = None
    #
    # def processMODIF(self):
    #     # Atualiza com MODIF
    #     for k,v in self.CONFHD.iteritems():
    #         if len(self.MODIF[k]) > 0:
    #             for n in range(len(self.MODIF[k])):
    #                 if 'VOLMIN' in self.MODIF[k][n]['tipo'].upper():
    #                     # Vem valor e unidade - real e % ou pu do volutil
    #                     # Tambem vem com unidade
    #                     if '%' in self.MODIF[k][n]['indice']:
    #                         # Calcula a pct do voloper para depois definir
    #                         tvolmax = float(self.VOLMAX[k])
    #                         tvolmin = float(self.VOLMIN[k])
    #                         volnew = (tvolmax - tvolmin) * (float(self.MODIF[k][n]['modif'])/100.0) + tvolmin
    #                         self.VOLMIN[k] = volnew
    #                     else:
    #                         self.VOLMIN[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'VOLMAX' in self.MODIF[k][n]['tipo'].upper():
    #                 # Vem valor e unidade - real e % ou pu do volutil
    #                 # Tambem vem com unidade
    #                 if '%' in self.MODIF[k][n]['indice']:
    #                     # Calcula a pct do voloper para depois definir
    #                     tvolmax = float(self.VOLMAX[k])
    #                     tvolmin = float(self.VOLMIN[k])
    #                     volnew = (tvolmax - tvolmin) * (float(self.MODIF[k][n]['modif'])/100.0) + tvolmin
    #                     self.VOLMAX[k] = volnew
    #                 else:
    #                     self.VOLMAX[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'VAZMIN' in self.MODIF[k][n]['tipo'].upper():
    #                     self.DEFMIN[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'IP' in self.MODIF[k][n]['tipo'].upper():
    #                     self.IP[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'TEIF' in self.MODIF[k][n]['tipo'].upper():
    #                     self.TEIF[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'PRODESP' in self.MODIF[k][n]['tipo'].upper():
    #                     self.PRODESP[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'PERDHIDR' in self.MODIF[k][n]['tipo'].upper():
    #                     self.PERDHIDR[k] = float(self.MODIF[k][n]['modif'])
    #                 elif 'NUMBAS' in self.MODIF[k][n]['tipo'].upper():
    #                     self.NUMBAS[k] = int(self.MODIF[k][n]['modif'])
    #                 elif 'NUMCNJ' in self.MODIF[k][n]['tipo'].upper():
    #                     self.NUMCNJ[k] = int(self.MODIF[k][n]['modif'])
    #                 elif 'NUMMAQ' in self.MODIF[k][n]['tipo'].upper():
    #                     self.NUMMAQ[k][int(self.MODIF[k][n]['modif'][1])-1] = int(self.MODIF[k][n]['modif'][0])
    #                 elif 'POTEFE' in self.MODIF[k][n]['tipo'].upper():
    #                     self.POTEFE[k][int(self.MODIF[k][n]['modif'][1])-1] = int(self.MODIF[k][n]['modif'][0])
    #                 elif 'CFUGA' in self.MODIF[k][n]['tipo'].upper():
    #                 idxupd = getUpdateIndexes(mes_i=self.MODIF[k][n]['mes'],
    #                                           ano_i=self.MODIF[k][n]['ano'],
    #                                           mes_f=self.MODIF[k][n]['mes'],
    #                                           ano_f=self.MODIF[k][n]['ano'],dger=self.DGER)
    #                 for idx in idxupd:
    #                     self.CFUGA[k][idx] = float(self.MODIF[k][n]['modif'])
    #                 elif 'VMINT' in self.MODIF[k][n]['tipo'].upper():
    #                     # Vem valor e unidade - real e % ou pu do volutil
    #                     # Tambem vem com unidade
    #                     idxupd = getUpdateIndexes(mes_i=self.MODIF[k][n]['mes'],
    #                                           ano_i=self.MODIF[k][n]['ano'],
    #                                           mes_f=self.MODIF[k][n]['mes'],
    #                                           ano_f=self.MODIF[k][n]['ano'],dger=self.DGER)
    #                     if '%' in self.MODIF[k][n]['indice']:
    #                         # Calcula a pct do voloper para depois definir
    #                         tvolmax = float(self.VOLMAX[k])
    #                         tvolmin = float(self.VOLMIN[k])
    #                         volnew = (tvolmax - tvolmin) * (float(self.MODIF[k][n]['modif'])/100.0) + tvolmin
    #                         for idx in idxupd:
    #                         self.VMINT[k][idx] = volnew
    #                     else:
    #                         for idx in idxupd:
    #                         self.VMINT[k][idx] = float(self.MODIF[k][n]['modif'])
    #                 elif 'VMAXT' in self.MODIF[k][n]['tipo'].upper():
    #                     # Vem valor e unidade - real e % ou pu do volutil
    #                     # Tambem vem com unidade
    #                     idxupd = getUpdateIndexes(mes_i=self.MODIF[k][n]['mes'],
    #                                                   ano_i=self.MODIF[k][n]['ano'],
    #                                                   mes_f=self.MODIF[k][n]['mes'],
    #                                                   ano_f=self.MODIF[k][n]['ano'],dger=self.DGER)
    #                     if '%' in self.MODIF[k][n]['indice']:
    #                         # Calcula a pct do voloper para depois definir
    #                         tvolmax = float(self.VOLMAX[k])
    #                         tvolmin = float(self.VOLMIN[k])
    #                         volnew = (tvolmax - tvolmin) * (float(self.MODIF[k][n]['modif'])/100.0) + tvolmin
    #                         for idx in idxupd:
    #                         self.VMAXT[k][idx] = volnew
    #                     else:
    #                         for idx in idxupd:
    #                     self.VMAXT[k][idx] = float(self.MODIF[k][n]['modif'])
    #                 elif 'VAZMINT' in self.MODIF[k][n]['tipo'].upper():
    #                     idxupd = getUpdateIndexes(mes_i=self.MODIF[k][n]['mes'],
    #                                               ano_i=self.MODIF[k][n]['ano'],
    #                                               mes_f=self.MODIF[k][n]['mes'],
    #                                               ano_f=self.MODIF[k][n]['ano'],dger=self.DGER)
    #                     for idx in idxupd:
    #                         self.VAZMINT[k][idx] = float(self.MODIF[k][n]['modif'])
    #                 elif 'COEFEVAP' in self.MODIF[k][n]['tipo'].upper():
    #                     info('   ******  MODIF: Alteracao de Coeficientes de Evaporacao  ****** ')
    #                     raise ValueError('leitura de MODIF de coeficientes de evaporacao nao implementada')
    #                 elif 'COTAREA' in self.MODIF[k][n]['tipo'].upper():
    #                     info('   ******  MODIF: Alteracao de Pol. Cota x Area  ****** ')
    #                     raise ValueError('leitura de MODIF de Pol. Cota x Area nao implementada')
    #                 elif 'VOLCOTA' in self.MODIF[k][n]['tipo'].upper():
    #                     info('   ******  MODIF: Alteracao de Pol. Vol x Cota  ****** ')
    #                     raise ValueError('leitura de modif de Pol. Vol x Cota  nao implementada')
    #                 elif 'VMINP' in self.MODIF[k][n]['tipo'].upper():
    #                     info('   ******  MODIF: Alteracao de VMINP  ****** ')
    #                     raise ValueError('leitura de modif de VMINP nao implementada')
    #
    # def preparePosMODIFDataStructs(self):
    #     self.INDISP = dict()
    #     self.EVAPT = dict()
    #     self.DEFMINT = dict()
    #     for k,v in self.CONFHD.iteritems():
    #         self.INDISP[k] = (1.0 - self.TEIF[k]/100.0) * (1.0 - self.IP[k]/100.0)
    #         self.EVAPT[k] = [0.0] * self.ni()
    #         idxev = self.mi() - 1
    #         for j in range(self.ni()):
    #             self.EVAPT[k][j] = self.EVAP[k][idxev]
    #             idxev += 1
    #             if idxev > 11:
    #                 idxev = 0
    #             # Ajusta DSVAGUA como no HSIM
    #             if self.DSVAGUA[k][j] != 0.0:
    #                 self.DSVAGUA[k][j] = self.DSVAGUA[k][j] * -1
    #         self.DEFMINT[k] = [self.DEFMIN[k]] * self.ni()
    #
    # def processEXPH(self):
    #     self.SerieNUMMAQ = dict()
    #     self.SeriePOTH = dict()
    #     for k,v in self.CONFHD.iteritems():
    #         exis = v['uexis']
    #         if exis in ['EE','EX']:
    #             totmaq = list([ dict(self.NUMMAQ[k]) for x in range(self.ni()) ])
    #             totpot = list()
    #             for x in range(self.ni()):
    #                 dtpot = dict()
    #                 for cj in range(self.NUMCNJ[k]):
    #                     if self.NUMMAQ[k][cj] == 0:
    #                         dtpot[cj] = 0.0
    #                     else:
    #                         dtpot[cj] = self.POTEFE[k][cj]
    #                 totpot.append(dict(dtpot))
    #         elif exis in ['NE']:
    #             tmaq = dict()
    #             tpot = dict()
    #             for n in range(self.NUMCNJ[k]):
    #                 tmaq[n] = 0
    #                 tpot[n] = 0.0
    #             totmaq = [ dict(tmaq) for xinc in range(self.ni()) ]
    #             totpot = [ dict(tpot) for xinc in range(self.ni()) ]
    #             self.SerieNUMMAQ[k] = totmaq
    #             self.SeriePOTH[k] = totpot
    #     # Aplicar alteracoes de motorizacao
    #     for k,v in self.MOTORI.iteritems():
    #         for d in v:
    #         mup = d['data'].split('/')[0]
    #         yup = d['data'].split('/')[1]
    #         idxatua = getUpdateIndexes(mes_i=mup,
    #                            ano_i=yup,
    #                            mes_f=12,
    #                            ano_f=self.DGER['yph'][-1], dger=self.DGER)
    #         if d['conj'] and d['maq']:
    #             # Formato novo de EXPH
    #             # Define o cnj e o maq sempre incremental
    #             cnj = d['conj'] - 1
    #             nmaqval = self.SerieNUMMAQ[k][idxatua[0]][cnj] + 1
    #             npotval = self.SeriePOTH[k][idxatua[0]][cnj] + float(d['pot'])
    #         else:
    #             # Formato antigo, verifica a pot que entra para identificar o cnj
    #             for ncnj in range(self.NUMCNJ[k]):
    #             if round(self.POTEFE[k][ncnj]) == round(float(d['pot'])):
    #                 cnj = ncnj
    #                 break
    #             # Definiu o cnj
    #             #print 'k = ',k
    #             #print 'cnj =',cnj
    #             #print self.SerieNUMMAQ[k]
    #             nmaqval = self.SerieNUMMAQ[k][idxatua[0]][cnj] + 1
    #             npotval = self.SeriePOTH[k][idxatua[0]][cnj] + float(d['pot'])
    #         for idx in idxatua:
    #             self.SerieNUMMAQ[k][idx][cnj] = nmaqval
    #             self.SeriePOTH[k][idx][cnj] = npotval
    #     # Aplicar alteracoes referentes ao enchimento de volume morto
    #     cvolm = 0.5
    #     for k,v in self.ENCHVM.iteritems():
    #         # Pct do volume morto cheio ate o momento
    #         volpct = float(v['pct'])
    #         # Numero de meses para enchimento
    #         nmeses = int(v['durmeses'])
    #         # Volume cheio ate o momento segundo a indicacao no EXPH
    #         volini = (volpct/100.0) * self.VOLMIN[k]
    #         # Valor de enchimento mensal considerando o que falta divido pelo nmeses
    #         venchmes = ((self.VOLMIN[k]-volini)/nmeses)
    #         # Definir vol ate a data de inicio enchimento
    #         mini = int(v['iniench'].split('/')[0])
    #         yini = int(v['iniench'].split('/')[1])
    #         idxatua = getUpdateIndexes(mes_i=self.mi(),
    #                                    ano_i=self.DGER['yph'][0],
    #                                    mes_f=mini,
    #                                    ano_f=yini, dger=self.DGER)
    #         for idx in idxatua:
    #             self.VMINT[k][idx] = volini
    #
    #         # Definir o enchimento em meses
    #         # utilizar um fator para parametrizacao de variacao
    #         # o VMINT varia ainda no mes final, em que para VMAXT esta o valor cheio
    #         yfim = yini
    #         mfim = mini
    #         for ycount in range(nmeses-1):
    #             mfim += 1
    #             if mfim > 12:
    #                 yfim += 1
    #                 mfim = 1
    #             for nmi in range(mini,mini+nmeses):
    #             mfim = nmi
    #             if nmi > 12:
    #                 mfim = 1
    #         idxatua = getUpdateIndexes(mes_i=mini,
    #                                    ano_i=yini,
    #                                    mes_f=mfim,
    #                                    ano_f=yfim, dger=self.DGER)
    #         #fatvm = 0.05
    #         fatvm = 0.0
    #         for n,midx in enumerate(idxatua):
    #             self.VMAXT[k][midx] = venchmes * (n+1) * (1.0+fatvm)
    #             self.VMINT[k][midx] = venchmes * (n+1) * (1.0-fatvm)
    #         intcheio = idxatua[-1]
    #         for icheio in range(intcheio,self.ni()):
    #             self.VMAXT[k][icheio] = self.VOLMAX[k]
    #             self.VMINT[k][icheio] = self.VOLMIN[k]
    #             self.VMINT[k][idxatua[-1]] = self.VOLMIN[k] * (1.0-fatvm)
    #
    #         # Ajustando EVAP e DSVAGUA(USO) para quando ainda nao encheu
    #         # Considerando que nao se aplicariam
    #         idxatua = getUpdateIndexes(mes_i=self.mi(),
    #                                    ano_i=self.yi(),
    #                                    mes_f=mfim,
    #                                    ano_f=yfim, dger=self.DGER)
    #
    #         for n,midx in enumerate(idxatua):
    #             self.DSVAGUA[k][midx] = 0.0
    #             self.EVAPT[k][midx] = 0.0
    #
    # def processThermalPlants(self):
    #     self.FCMAX = dict()
    #     self.IPTER = dict()
    #     self.TEIFT = dict()
    #     self.GTMIN = dict()
    #     self.COMB = dict()
    #     self.tPOT = dict()
    #     self.tPOTINST = dict()
    #     self.CUST = dict()
    #
    #     for k,v in self.CONFT.iteritems():
    #         self.FCMAX[k] = [float(self.TERM[k]['fcmax'])] * self.ni()
    #         #[float(self.TERM[k]['fcmax'])/100.00] * self.ni()
    #         self.IPTER[k] = [float(self.TERM[k]['ip'])] * self.ni()
    #         #[float(self.TERM[k]['ip'])/100.00] * self.ni()
    #         self.TEIFT[k] = [float(self.TERM[k]['teif'])] * self.ni()
    #         #[float(self.TERM[k]['teif'])/100.00] * self.ni()
    #
    #         gtm = list()
    #         for x in range(self.mi(),13):
    #         gtm.append(float(self.TERM[k]['gtmin'+str(x)]))
    #         for x in range(13 - self.mi(),self.ni()):
    #         gtm.append(float(self.TERM[k]['gtdmais']))
    #         self.GTMIN[k] = list(gtm)
    #
    #         self.COMB[k] = self.CLAST[k]['tipocomb']
    #
    #         # Thermal Unit Generation
    #         self.TUG = self.CADTERM[k]
    #
    #         # Carregar CUSTO
    #         cust = list()
    #         idxm = self.mi()
    #         idxc = 1
    #         for x in range(self.ni()):
    #         cust.append(float(self.CLAST[k]['custo'+str(idxc)]))
    #         idxm += 1
    #         if idxm > 12:
    #             idxm = 1
    #             idxc += 1
    #         self.CUST[k] = list(cust)
    #
    #         self.tPOT[k] = [float(self.TERM[k]['pot'])] * self.ni()
    #         self.tPOTINST[k] = float(self.TERM[k]['pot'])
    #     # adjust values
    #     # Atualizar custos segundo o CLAST
    #     mdifc = len(self.MODIFCLAST[k])
    #     if mdifc > 0:
    #         # Tem atualizacao de custo
    #         for x in range(mdifc):
    #         periodo = list()
    #         if self.MODIFCLAST[k][x]['mesf'] != '':
    #             periodo = getUpdateIndexes(mes_i=self.MODIFCLAST[k][x]['mesi'],
    #                                         ano_i=self.MODIFCLAST[k][x]['anoi'],
    #                                         mes_f=self.MODIFCLAST[k][x]['mesf'],
    #                                         ano_f=self.MODIFCLAST[k][x]['anof'],dger=self.DGER)
    #         else:
    #             periodo = getUpdateIndexes(mes_i=self.MODIFCLAST[k][x]['mesi'],
    #                                        ano_i=self.MODIFCLAST[k][x]['anoi'],
    #                                        mes_f=12,
    #                                        ano_f=self.DGER['yph'][-1],dger=self.DGER)
    #         for idx in periodo:
    #             self.CUST[idx] = float(self.MODIFCLAST[k][x]['custo'])
    #     # Atualizar com informacoes do EXPT
    #     mdift = len(self.EXPT[k])
    #     if mdift > 0:
    #         # Tem atualizacao de informacoes no EXPT
    #         for x in range(mdift):
    #         periodo = list()
    #         if self.EXPT[k][x]['mf'] != '':
    #             periodo = getUpdateIndexes(mes_i=self.EXPT[k][x]['mi'],
    #                                        ano_i=self.EXPT[k][x]['anoi'],
    #                                        mes_f=self.EXPT[k][x]['mf'],
    #                                        ano_f=self.EXPT[k][x]['anof'],dger=self.DGER)
    #         else:
    #             periodo = getUpdateIndexes(mes_i=self.EXPT[k][x]['mi'],
    #                                        ano_i=self.EXPT[k][x]['anoi'],
    #                                        mes_f=12,
    #                                        ano_f=self.DGER['yph'][-1],dger=self.DGER)
    #         txtmesf = self.EXPT[k][x]['mf']
    #         if txtmesf is '':
    #             txtmesf = 12
    #         txtanof = self.EXPT[k][x]['anof']
    #         if txtanof is '':
    #             txtanof = self.DGER['yph'][-1]
    #         # Aplicando alteracoes
    #         tpmodif = self.EXPT[k][x]['tipo']
    #         modifvalue = float(self.EXPT[k][x]['modif'])
    #         if tpmodif == 'GTMIN':
    #             for idx in periodo:
    #             self.GTMIN[idx] = modifvalue
    #         elif tpmodif == 'FCMAX':
    #             for idx in periodo:
    #             self.FCMAX[idx] = modifvalue
    #         elif tpmodif == 'POTEF':
    #             for idx in periodo:
    #             self.tPOT[idx] = modifvalue
    #         elif tpmodif == 'IPTER':
    #             for idx in periodo:
    #             self.IPTER[idx] = modifvalue
    #         elif tpmodif == 'TEIFT':
    #             for idx in periodo:
    #             self.TEIFT[idx] = modifvalue
    #     # Aplicar alteracoes de MANUTT
    #     # Estabelecendo anos considerados segundo o DGER, como especificado no manual
    #     # do NEWAVE
    #     nmanutt = len(self.MANUTT[k])
    #     if nmanutt > 0:
    #         for x in range(nmanutt):
    #         if int(self.MANUTT[k][x]['ano']) in self.DGER['yph'][0:self.DGER['nanomanutute']]:
    #             #print 'Uhe = ',k,' tem manutt'
    #             anoM = int(self.MANUTT[k][x]['ano'])
    #             mesM = int(self.MANUTT[k][x]['mes'])
    #             diaM = int(self.MANUTT[k][x]['dia'])
    #             datDur = datetime.timedelta(days=int(self.MANUTT[k][x]['dur'])-1)
    #             datamanu = datetime.date(anoM,mesM,diaM) + datDur
    #             mesesM = 1 + datamanu.month - int(mesM)
    #             for idxmM in range(mesesM):
    #             mesAfetado = mesM + idxmM
    #             idxpos = mesM - self.mi() + idxmM
    #             totDiasMesAfetado = calendar.monthrange(anoM,mesAfetado)[1]
    #             if idxmM == 0:
    #                 # primeiro mes
    #                 if mesesM > 1:
    #                 #Indice = (self.daysofMonth(mesManutt,anoManutt)-diaManutt)/self.daysofMonth(mesManutt,anoManutt)
    #                 Indice = float(totDiasMesAfetado - diaM +1) / float(totDiasMesAfetado)
    #                 else:
    #                 # So altera o mes corrente
    #                 Indice = float(self.MANUTT[k][x]['dur']) / float(totDiasMesAfetado)
    #             elif idxmM+1 == mesesM:
    #                 # ultimo mes
    #                 Indice = float(datamanu.day) / float(totDiasMesAfetado)
    #             else:
    #                 # mes intermediario
    #                 Indice = 1
    #
    #             newpot = float(self.tPOT[idxpos]) - (Indice * float(self.MANUTT[k][x]['pot']))
    #             if newpot < 0:
    #                 newpot = 0.0
    #             #print 'UHE ',k,self.CONFT[k]['nome'],' - pos:',idxpos,' - data:', self.MANUTT[k][x]['data'],' pot_ini:',nut.pot[idxpos],' pot_fim:',newpot
    #             self.tPOT[idxpos] = newpot
    #
    # def loadVAZData(self):
    #     self.VAZMLT = dict()
    #     self.VAZCEN = dict()
    #     self.VAZMAX = dict()
    #     yi = self.yi()
    #     mi = self.mi()
    #     ni = self.ni()
    #     # Ano de inicio de varredura para cenarios
    #     anoini = int(self.SHISTANO)
    #     # Calcular os meses para divisao dos somatorios
    #     nmes = [yi-self.DGER['hiy']] * 12
    #     for mesid in range(1,mi):
    #         nmes[mesid-1] += 1
    #     # Definir o ano final
    #     if mi < 2:
    #         yf = yi
    #     else:
    #         yf = yi+1
    #     for codusi,dados in self.CONFHD.iteritems():
    #         self.VAZCEN[codusi] = list()
    #         self.VAZMLT[codusi] = [0.0] * 12
    #         posto = int(dados['posto'])
    #         for year in range(self.DGER['hiy'],yf):
    #             for mesid in range(1,13):
    #                 self.VAZMLT[codusi][mesid-1] += self.VAZOES[posto][year][mesid]
    #         # Fazendo a media
    #         for n,fatmed in enumerate(nmes):
    #             self.VAZMLT[codusi][n] /= fatmed
    #         #self.histlen = sum(nmes)
    #         # Definir vazao maxima registrada no historico
    #         self.VAZMAX[codusi] = max(self.vaz[posto])
