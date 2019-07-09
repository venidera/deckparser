# Importação de Decks DESSEM

Neste documento são apresentados os procedimentos, arquivos importados
e sugestões de uso para os dados obtidos através dos decks do modelo
DESSEM produzido pelo CEPEL.

O importador consiste numa biblioteca que realiza a extração dos dados
contidos em um deck DESSEM e os converte para objetos na linguagem
Python, que podem ser utilizados para submissão como entrada em
modelos de simulação e otimização, e também podem ser exportados para
formatos mais amigáveis ou transacionais. Também é possível realizar a 
leitura dos resultados do modelo DESSEM.

Neste documento estaremos utilizando o conjunto de decks DESSEM CCEE
[*DES_201805.zip*](https://www.ccee.org.br/ccee/documentos/CCEE_640604)
que consiste dos decks do PMO de maio/2018.
Também foram realizados testes com o conjunto de decks do PMO de outubro/2018 
[*des_201810.zip*](https://www.ccee.org.br/ccee/documentos/DES_201810).

O formato dos arquivos contidos nos decks corresponde à especificação
que consta no Manual do Usuário da versão 12.2 do DESSEM. 

## Instalação do módulo Python

Para informações sobre a intalação do módulo Python veja o documento que descreve a [importação de decks DECOMP](Processo_de_importacao_de_um_deck_DECOMP.md).

## Extraindo dados para formato JSON

A forma mais simples de testar a instalação e o importador, é extrair
os dados utilizando o comando `dessem2json`, que possui a sintaxe
abaixo:

> Em sistemas Windows pode ser necessário alterar a extensão do arquivo *dessem2json* renomeando-o para *dessem2json.py*.
> Uma alternativa é usar o comando `python dessem2json`.

```
$ dessem2json -h
usage: dessem2json [-h] [-list_files] [-list_records dsfile] [-file ZIP_FILE]
                   [-list_cases] [-load_results] [-days d [d ...]]
                   [-grid_option {on,off,all}] [-ds_files rec [rec ...]]
                   [-ds_records rec [rec ...]] [-grid_intervals t [t ...]]
                   [-outfile f]

DESSEM deck files importer

optional arguments:
  -h, --help            show this help message and exit
  -list_files           List file that can be read
  -list_records dsfile  List records that can be read from the file type
                        "dsfile"
  -file ZIP_FILE        File containing DESSEM cases (decks)
  -list_cases           List cases contained in the given file
  -load_results         Load DESSEM results from the given file
  -days d [d ...]       Read only cases with dates corresponding to days
                        (default: all)
  -grid_option {on,off,all}
                        Read only cases containing grid data (on) or not (off)
                        (default: all)
  -ds_files rec [rec ...]
                        File types to be read (default: all)
  -ds_records rec [rec ...]
                        Records to be read (default: all)
  -grid_intervals t [t ...]
                        Grid data time intervals to be read (default: all)
  -outfile f            File to save imported data
--------------------------------------------------
Exemplos
--------------------------------------------------
- Lista de arquivos que podem ser lidos
>>>> dessem2json -list_files
- Lista de registros que podem ser lidos de um dado arquivo
>>>> dessem2json -list_records arquivo
- Lista de casos contidos no arquivo
>>>> dessem2json -list_cases -file DES_201805.zip
- Exportação de todos os decks contidos no arquivo fornecido
>>>> dessem2json -file DES_201805.zip
- Exportação dos decks com data 02/05/2018
>>>> dessem2json -file DES_201805.zip -days 2
- Exportação dos decks com datas 02/05/2018 e 05/05/2018
>>>> dessem2json -file DES_201805.zip -days 2 5
- Exportação do deck com rede elétrica
>>>> dessem2json -file DES_201805.zip -days 2 -grid_option on
- Exportação do arquivo entdados, contido no deck especificado
>>>> dessem2json -file DES_201805.zip -days 2 -grid_option on -ds_files entdados
- Exportação do registro UH do arquivo entdados
>>>> dessem2json -file DES_201805.zip -days 2 -grid_option on -ds_files entdados -ds_records UH
- Exportação dos dados de barramentos da rede elétrica básica* para o primeiro intervalo de tempo
>>>> dessem2json -file DES_201805.zip -days 2 -grid_option on -ds_files eletbase -ds_records DBAR -grid_intervals 1
- Exportação dos dados de modificação de barramentos da rede elétrica básica para o primeiro intervalo de tempo
>>>> dessem2json -file DES_201805.zip -days 2 -grid_option on -ds_files eletmodif -ds_records DBAR -grid_intervals 1
- Exportação de resultados
>>>> dessem2json -file DES_201805.zip -load_results

* Rede elétrica básica é aquela que não contém as modificações específicas para o intervalo de tempo dado
--------------------------------------------------
Arquivos disponíveis para leitura
--------------------------------------------------
Arquivos de índice: dessem, desselet
Arquivo com dados gerais do caso: entdados
Arquivos com dados das usinas hidrelétricas, rede hidráulica e restrições aplicáveis: hidr, operuh, dadvaz, curvtviag, cotasr11, ils_tri
Arquivos com dados para simulação: simul, deflant
Arquivos com dados sobre área de controle e reserva de potência: areacont, respot
Arquivos com dados da rede elétrica: eletbase, eletmodif
Arquivos com dados das usinas termelétricas: termdat, operut, ptoper
Arquivos com dados outras usinas: renovaveis
Outros arquivos: infofcf, tolperd
Arquivos com resultados: pdo_operacao, pdo_sist, pdo_sumaoper
```

Por exemplo, a saída para a extração do registro *UH* do arquivo *entdados*, do dia 02/05/2018 (sem rede) fica:

```
$ dessem2json DES_201805.zip -days 2 -grid_option off -ds_files entdados -ds_records UH
Loading case for date 2018-05-02 Sem Rede
{
 "2018-05-02": {
  "sem_rede": {
   "entdados": {
    "UH": [
     {
      "nomeCampo": "UH",
      "idUsina": 1,
      "nomeUsina": "CAMARGOS",
      "idREE": 10,
      "volumeInicial": 85.51,
      "flagEvap": 1,
      "diaIni": "I",
      "horaIni": null,
      "meiaHoraIni": null,
      "volumeMorto": 0.0,
      "flagProdutivCte": 0,
      "flagRestrBangBang": 0
     },
     {
      "nomeCampo": "UH",
      "idUsina": 2,
      "nomeUsina": "ITUTINGA",
      "idREE": 10,
      "volumeInicial": 99.95,
      "flagEvap": 1,
      "diaIni": "I",
      "horaIni": null,
      "meiaHoraIni": null,
      "volumeMorto": 0.0,
      "flagProdutivCte": 0,
      "flagRestrBangBang": 0
     },
      ...
```

## Estrutura do importador

O importador dos decks do DESSEM está localizado no pactote *deckparser.importers.dessem*, 
que possui os seguintes pacotes:

- Pacote *cfg*: contém os arquivos de configuração, em formato xml, que determina 
a estrutura dos dados contidos em cada arquivo do deck. Cada arquivo xml contém:

	- Atributo *name*: nome de identificação do tipo de arquivo;
	- Conjunto de elementos tipo *record* e/ou *table*, cada um contendo:
		- Atributo *name*: nome do registro;
		- Conjunto de elementos tipo *field*, que identificam cada campo do registro, 
			contendo:
			- Atributos: nome (*name*), tipo de dado (*type*), valor default (*default*) e 
				valores especiais (*special*)
			- Elemento com validações (*validation*), 
			- Estrutura de campos compostos (*composed=True*).

- Pacote *core*: cotém os módulos que realizam os métodos fundamentais utilizados 
na importação, as principais classes destes módulos são:

	- *xmlReader*: responsável por fazer a leitura dos arquivos de configuração;
	- *record*: classe que representa a estrutura de dados de cada registro dos arquivos do deck.
		É responsável por fazer a leitura de todos os campos;
	- *table*: realiza a leitura dos resgitros múltiplos e armzena os dados lidos em uma lista;
	- *dsFile*: classe abstrata que é estendida pelas classes importadoras, que por sua vez 
		realizam a importação dos dados de cada arquivo do deck. A função desta classe é fazer a 
		leitura de todos os registros do arquivo;
	- O pacote *core* ainda contém o módulo *dataType*, que contém métodos para decodificar
		e validar cada tipo de dado.

O arquivo *hidr*, por ser um arquivo não formatado (codificado), possui metodologia de 
leitura especifica.

Cada módulo localizado no pacote *dessem* contém uma classe que realiza a importação 
de um arquivo específico. O conjunto de arquivos que podem ser lidos é:

- Arquivos de indice:
	- *dessem*: índice dos arquivos contidos no decks;
	- *desselet*: dados sobre os intervalos de tempo e índice dos arquivos que contém os dados
		da rede elétrica: para cada caso base (patamar de carga); e as alterações de rede elétrica 
		aplicadas especificamente para cada intervalo de tempo;

- Arquivo com dados gerais do caso:
	- *entdados*: dados diversos sobre cada elemento do sistema, além de dados sobre a 
		configuração dos intervalos de tempo, entre outras opções de configuração do estudo;

- Arquivos com dados das usinas hidrelétricas, rede hidráulica e restrições aplicáveis:
	- *hidr*:  dados cadastrais e construtivos das usinas hidrelétricas;
	- *operuh*: dados sobre as restrições de operação hidraúlica;
	- *dadvaz*: dados sobre as vazões naturais afluentes ao longo do período de interesse;
	- *curvtviag*: dados sobre a propagação da água entre usinas hidrelétricas;
	- *cotasr11*: cotas na régua 11 anteriores ao início do estudo;
	- *ils_tri*: dados de vazão no canal Pereira Barreto (entre as usinas de Ilha Solteira e Três Irmãos);

- Arquivos com dados para simulação (período de pré-interesse):
	- *simul*: dados sobre a simulação hidráulica anterior ao período de interesse;
	- *deflant*: dados sobre as vazões defluentes anteriores ao início do período de interesse;

- Arquivos com dados sobre área de controle e reserva de potência:
	- *areacont*: dados das áreas de controle;
	- *respot*: dados sobre reserva de potência mínima;

- Arquivos com dados da rede elétrica:
	- *eletbase*: dados básicos da rede elétrica para cada caso (patamar de carga);
	- *eletmodif*: dados sobre as modificações da rede elétrica aplicadas em cada 
		intervalo de tempo;

- Arquivos com dados das usinas termelétricas:
	- *termdat*: dados cadastrais e construtivos das usinas termelétricas;
	- *operut*: dados sobre a operação termelétrica, inclusive restrições;
	- *ptoper*: dados sobre a operação de usinas que não são decididos pelo modelo DESSEM
		(atualmente somente a leitura dos dados sobre a geração termelétrica antecipada 
		está configurada);

- Arquivos com dados de outras usinas:
	- *renovaveis*: dados cadastrais de usinas e geração a partir de fontes renováveis;

- Outros arquivos:
	- *infofcf*: dados sobre a função de custo futuro do DECOMP;
	- *tolperd*: dados sobre a tolerência para convergência do valor das perdas elétricas;

- Arquivos cuja leitura não está implementada (codificados):
	- *mlt*: dados sobre média de longo termo das vazões naturais afluentes;
	- *mapcut*: dados sobre a função de custo futuro do DECOMP;

- Pacote *out*: cotém os módulos que realizam a leitura dos arquivos com resultados, sendo
possível a leitura dos seguintes arquivos:
	- *pdo_operacao*: conjunto de resultados da solução obtida com o modelo DESSEM, 
	fornecidas para cada intervalo de tempo;
	- *pdo_sist*: resultados referentes a cada subsistema, por intervalo de tempo;
	- *pdo_sumaoper*: resultados agregados por dia e por semana;

O módulo *util* contém alguns métodos destinados a realizar testes.
O módulo *teste* contém exemplos de testes. 

## Executando a importação

A importação dos dados em objetos do tipo `dict` é realizada utilizando o método 
*desssem2dicts*, a sintaxe deste é método é a seguinte:
```python
>>>> from deckparser.dessem2dicts import dessem2dicts
>>>> dc = desssem2dicts(fn, dia, rd, [file_filter, interval_list, file_encoding, load_results])
```

Onde:

- `fn`: é o caminho para o arquivo compactado que contém os decks do DESSEM

- `dia`: especifica os dias que deverão ser lidos, pode ser:
	- Dia do mês (`int`);
	- Data (`datetime.date(Y,m,d)`);
	- `list` contendo objetos do tipo `int` ou `datetime.date`;
	- `None` (todos os dias encontrados no arquivo)

- `rd`: especifica se devem ser lidos os casos com rede (`True`), sem rede (`False`) 
	ou ambos (`None` ou `[True,False]`)
	
- O parâmetro `file_filter` deve ser do tipo `dict`, conforme o padrão:
```
{arquivo: list(registro)}
Exemplo: {'entdados': ['UH', 'UT']}
```

- O parâmetro `interval_list` deve ser do tipo `list`, contendo os índices (`int`) de cada
intervalo de tempo (conforme a especificação no arquivo desselet) a serem lidos. Caso 
seja feita a leitura dos arquivos do tipo *eletbase* deve-se notar que o resultado é
fornecido com os índices correspondentes a cada caso base selecionado, por exemplo, 
os índices [1,2] podem corresponder ao mesmo caso base de índice 1 

- `file_encoding`: especifica a codificação para leitura dos arquivos (`str` ou `list(str)`)
- `load_results`: determina que devem ser lidos os arquivos de saída, resultados do modelo DESSEM

O arquivo (compactado) fornecido deve conter arquivos também compactados (casos), 
cada um destes contendo os arquivos do deck. Cada caso deve possuir nome conforme o 
padrão:
```
DES_CCEE_(yyyy)(mm)(dd)_(Com|Sem)Rede.zip
```

Onde:

- `yyyy`, `mm`, `dd`: são ano, mês e dia do caso;

- `Com` (`Sem`): indica se o caso considera (ou não) a rede elétrica.

O padrão acima mencionado também pode assumir a seguinte forma, sendo identificado
de forma automática:
```
DS_CCEE_(mm)(yyyy)_(COM|SEM)REDE_RV(r)D(dd).zip
```

Onde:

- `yyyy`, `mm`, `dd`: são ano, mês e dia do caso;

- `r`: é a revisão do PMO;

- `COM` (`SEM`): indica se o caso considera (ou não) a rede elétrica.

Quando a opção de leitura dos arquivos de saída está ativa, são lidos os
arquivos com nome em padrão semelhante, porém iniciados com o prefixo
`Resultado_`.

O resultado da leitura é o um objeto `dict` com a seguinte estrutura:
```
{dia: {r: caso:dict}}
Exemplo: {date(2018,05,25): {True: casoComRede, False: casoSemRede}}
```

Onde:

- `dia`: é um objeto do tipo `date`

- `r`: indica se o caso considera rede elétrica (`bool`)

O conjunto de dados de cada caso possui a seguinte estrutura:
```
{arquivo: {(registro|tabela): (dados:(dict|list))}
Exemplo: {'entdados': {'UH': dados, ...}}
```

O conjunto de dados de cada registro é estruturado na forma:
```
{campo: valor}
Exemplo: {'idUsina': 66, 'nomeUsina': 'ITAIPU', ...}
```

Caso o resgitro seja múltiplo (tabela), os dados são fornecidos em um objeto do tipo `list`, 
contendo um objeto `dict` (conforme a estrutura acima) para cada registro lido.

Os dados do arquivo *hidr* são armazenados em um único registro (UHE):
```
{'hidr': {'UHE': list}}
```

A classe Loader é responsável por realizar o carregamento dos dados de um deck. 
O código abaixo realiza a leitura do caso contido no diretório `dr` e armazena 
o resultado da leitura em `dc`:

```python
>>> from deckparser.importers.dessem.loader import Loader
>>> 
>>> ld = Loader(dr)
>>> ld.loadAll()
>>> dc = ld.toDict()
```

Caso ocorram erros de validação ou de leitura dos dados, os mesmos são reportados via logging
e o carregamento dos dados continua normalmente. Caso não seja possível carregar um deck, 
o processo continua sem armazenar o caso correspondente.  

## Atualizações

O processo de importação segue em atualização visto que o modelo
DESSEM está em evolução contínua. Assim, sempre que necessário ou que um
novo dado é adicionado o importador é atualizado para contemplar o
dado na importação caso seja de interesse para uso no modelo ODIN-H.
