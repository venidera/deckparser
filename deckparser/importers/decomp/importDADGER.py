from deckparser.importers.imputils import searchInList, getUpdateIndexes
from logging import info,debug

def importDADGER(data):
    DADGER = {
        'UH': [], 'CT': [], 'UE': [], 'DP': []
    }

    for line in data:
        if line[0]=='&':
            continue

        id = line[0:2].strip()
        if id == "UH":
            DADGER["UH"].append(importUH(line))
        elif id == "CT":
            DADGER["CT"].append(importCT(line))
        elif id == "UE":
            DADGER["UE"].append(importUE(line))
        elif id == "DP":
            DADGER["DP"].append(importDP(line))

    return DADGER

#      else if(id == "PQ")
#        ContaDadosGerPQ(Data->Strings[i],GeracaoPCH);
#      else if(id == "IT")
#        ImportDadosGerIT(Data->Strings[i]);
#      else if(id == "IA")
#        ImportDadosGerIA(Data->Strings[i]);
#      else if(id == "TX")
#        TxDesconto = Data->Strings[i].SubString(5,5).Trim().ToDouble();
#      else if(id == "DT")
#        IniDecomp = TDateTime(Data->Strings[i].SubString(15,4).Trim().ToInt(),
#                              Data->Strings[i].SubString(10,2).Trim().ToInt(),
#                              Data->Strings[i].SubString(5,2).Trim().ToInt());
#      else if(id == "MP" || id == "VE" || id == "VM" || id == "DF" || id == "TI")
#        ImportDadosGerMPVEVMDFTI(id, Data->Strings[i]);
#      else if(id == "MT")
#	      ImportDadosGerMT(Data->Strings[i]);
#      else if(id == "VI")
#        ImportDadosGerVI(Data->Strings[i],PrimeiroVI);
#      else if(id == "RE")
#	      ImportDadosGerRE(Data->Strings[i]);
#      else if(id == "LU")
#	      ImportDadosGerLU(Data->Strings[i]);
#      else if(id == "FU")
#	      ImportDadosGerFU(Data->Strings[i]);
#      else if(id == "FT")
#	      ImportDadosGerFT(Data->Strings[i]);
#      else if(id == "FI")
#	      ImportDadosGerFI(Data->Strings[i]);
#      else if(id == "AC")
#        ImportDadosGerAC(Data->Strings[i]);
#      else
#        // pula registros desconhecidos
#        continue;

#    ImportDadosGerPQ(GeracaoPCH);


def ConvCodUteFromDecomp(CodUte):
    if CodUte==6:
        CodUte = 66
    return CodUte
    
def importUH(line):
    return {
        'CodUhe': int(line[4:7].strip()),
        'VolIni': float(line[14:24].strip())
    }

def importCT(line):
    return {
        'CodUte': ConvCodUteFromDecomp(int(line[4:7].strip())),
        'Estagio': int(line[24:26].strip()),
        'GTMIN': [float(line[29:34].strip()),
                  float(line[49:54].strip()),
                  float(line[69:74].strip())],
        'POTEF': [float(line[34:39].strip()),
                  float(line[54:59].strip()),
                  float(line[74:79].strip())],
        'CUSTO': [float(line[39:49].strip()),
                  float(line[59:69].strip()),
                  float(line[79:89].strip())],
    }

#  ImportUteDados(CodUte,UGT_ID,"TEIF",1,Ini,Fim,0,Estagio);
#  ImportUteDados(CodUte,UGT_ID,"TEIF",2,Ini,Fim,0,Estagio);
#  ImportUteDados(CodUte,UGT_ID,"TEIF",3,Ini,Fim,0,Estagio);

#  ImportUteDados(CodUte,UGT_ID,"IPTER",1,Ini,Fim,0,Estagio);
#  ImportUteDados(CodUte,UGT_ID,"IPTER",2,Ini,Fim,0,Estagio);
#  ImportUteDados(CodUte,UGT_ID,"IPTER",3,Ini,Fim,0,Estagio);

#  ImportUteDados(CodUte,UGT_ID,"FCMAX",1,Ini,Fim,100,Estagio);
#  ImportUteDados(CodUte,UGT_ID,"FCMAX",2,Ini,Fim,100,Estagio);
#  ImportUteDados(CodUte,UGT_ID,"FCMAX",3,Ini,Fim,100,Estagio);

def importUE(line):
    return {
        'Nome': line[14:26].strip(),
        'Jusante': int(line[29:32].strip()),
        'Montante': int(line[34:37].strip()),
        'VazMin': float(line[39:49].strip()),
        'VazMax': float(line[49:59].strip()),
        'Consumo': float(line[59:69].strip())
    }

#  Query->SQL->Clear();
#  Query->SQL->Add("SELECT CodUsina FROM Desvio ");
#  Query->SQL->Add("WHERE CodUsina=:CodUsina AND CodJus=:CodJus");
#  Query->ParamByName("CodUsina")->AsInteger = ConvTab[Montante-1];
#  Query->ParamByName("CodJus")->AsInteger = ConvTab[Jusante-1];
#  if(!Query->Prepared)
#    Query->Prepare();
#  Query->Open();

#  bool found = (Query->RecordCount>0);

#  Query->Close();
#  Query->SQL->Clear();

#  if(found)
#  {
#    Query->SQL->Add("UPDATE Desvio ");
#    Query->SQL->Add("SET DefMin=:DefMin,DefMax=:DefMax,ConsEsp=:ConsEsp,Nome=:Nome ");
#    Query->SQL->Add("WHERE CodUsina=:CodUsina AND CodJus=:CodJus ");

#  }
#  else
#  {
#    Query->SQL->Add("INSERT INTO Desvio ");
#    Query->SQL->Add("(CODUSINA,CODJUS,DEFMIN,DEFMAX,CONSESP,NOME) ");
#    Query->SQL->Add("VALUES (:CodUsina,:CodJus,:DefMin,:DefMax,:ConsEsp,:Nome)");
#  }

#  Query->ParamByName("CodUsina")->AsInteger = ConvTab[Montante-1];
#  Query->ParamByName("CodJus")->AsInteger = ConvTab[Jusante-1];
#  Query->ParamByName("DefMin")->AsFloat = VazMin;
#  Query->ParamByName("DefMax")->AsFloat = VazMax;
#  Query->ParamByName("ConsEsp")->AsFloat = Consumo;
#  Query->ParamByName("Nome")->AsString = Nome;
#  if(!Query->Prepared)
#    Query->Prepare();
#  Query->ExecSQL();

def importDP(line):
    DP = {
        'Estagio': int(line[4:6].strip()),
        'CodSubsistema': int(line[9:11].strip()),
        'NumPatamares': int(line[14:15].strip()),
        'Duracao': []
    }
    
    mercado = []
    
    for patamar in range(1,DP['NumPatamares']+1):
        startPos = patamar*20-1
        carga = line[startPos:startPos+10].strip()
        if carga != "":
            carga = float(carga)
            mercado.append(carga)

        DP['Duracao'].append(float(line[startPos+10:startPos+20].strip()))
        #    DuracaoTotal += Duracao[Patamar-1];

    if len(mercado)>0:
        DP['MMED'] = mercado

    return DP
#  int TPD_ID = GetTpdId("MMED");
#  double Carga, Duracao[3], DuracaoTotal = 0;



#  if(EstagioList->IndexOf((void *)Estagio)==-1)
#  {
#    EstagioList->Add((void *)Estagio);
#    for(int Patamar=1; Patamar <= NumPatamares; Patamar++)
#      ImportPatamarDuracao(Patamar,Ini,Duracao[Patamar-1]/DuracaoTotal,Estagio);
#  }
#}
#//---------------------------------------------------------------------------
#void __fastcall
#TFormDlgImportNewave::ContaDadosGerPQ(const AnsiString Line, TList *GeracaoPCH)
#{
#  int CodSubsistema = Line.SubString(15,2).Trim().ToInt();
#  int Estagio = Line.SubString(20,2).Trim().ToInt();
#  double Valor[3] = {Line.SubString(25,5).Trim().ToDouble(),
#                    Line.SubString(30,5).Trim().ToDouble(),
#                    Line.SubString(35,5).Trim().ToDouble()};
#  GeracaoPCHItem *Item;

#  for(int i=0; i<GeracaoPCH->Count; i++)
#  {
#    Item = (GeracaoPCHItem *) GeracaoPCH->Items[i];
#    if(Item->CodSubsistema == CodSubsistema &&
#       Item->Estagio == Estagio)
#    {
#      for(int j=0; j < 3; j++)
#        Item->Valor[j] += Valor[j];
#      return;
#    }
#  }

#  Item = new GeracaoPCHItem;
#  Item->CodSubsistema = CodSubsistema;
#  Item->Estagio = Estagio;
#  for(int j=0; j < 3; j++)
#    Item->Valor[j] = Valor[j];
#  GeracaoPCH->Add((void *)Item);
#}
#//---------------------------------------------------------------------------
#void __fastcall
#TFormDlgImportNewave::ImportDadosGerPQ(TList *GeracaoPCH)
#{
#  GeracaoPCHItem *Item;

#  for(int i=0; i<GeracaoPCH->Count; i++)
#  {
#    Item = (GeracaoPCHItem *) GeracaoPCH->Items[i];
#    for(int j=0; j < 3; j++)
#      ImportDadoGeracaoPCH(Item->CodSubsistema,Ini,Item->Valor[j],j+1,Item->Estagio);
#    delete Item;
#  }
#}
#//---------------------------------------------------------------------------
#void __fastcall
#TFormDlgImportNewave::ImportDadosGerIT(const AnsiString Line)
#{
#  int Patamar;
#  double Mande, GerIt50;

#  // importa carga Ande na tabela MERCADO
#  int TPD_MANDE = GetTpdId("MANDE");
#  int TPD_IMED = GetTpdId("IMED");
#  int Estagio = Line.SubString(5,2).Trim().ToInt();
#  for(Patamar=1; Patamar<=3; Patamar++)
#  {
#    GerIt50 = Line.SubString(10+Patamar*10,5).Trim().ToDouble();
#    Mande = Line.SubString(15+Patamar*10,5).Trim().ToDouble();
#    ImportDadoMercado(sstITAIPU,TPD_MANDE,Patamar,Ini,Fim,Mande,Estagio);
#    ImportDadoIntercambio(Patamar,TPD_IMED,sstITAIPU,sstFicSul,Ini,Fim,GerIt50,Estagio);
#    ImportDadoIntercambio(Patamar,TPD_IMED,sstFicSul,sstITAIPU,Ini,Fim,0,Estagio);
#    ImportDadoIntercambio(Patamar,TPD_IMED,sstITAIPU,sstSECO,Ini,Fim,99999,Estagio);
#    ImportDadoIntercambio(Patamar,TPD_IMED,sstSECO,sstITAIPU,Ini,Fim,0,Estagio);
#  }
#}

