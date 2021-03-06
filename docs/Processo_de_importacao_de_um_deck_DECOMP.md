# Importação de Decks DECOMP

Neste documento são apresentados os procedimentos, arquivos importados
e sugestões de uso para os dados obtidos através dos decks do modelo
DECOMP produzido pelo CEPEL.

O importador consiste numa biblioteca que realiza a extração dos dados
contidos em um deck DECOMP e os converte para objetos na linguagem
Python, que podem ser utilizados para submissão como entrada em
modelos de simulação e otimização, e também podem ser exportados para
formatos mais amigáveis ou transacionais.

Adicionalmente uma ferramenta de linha de comando denominada
*decomp2json* permite extrair estes dados em formato JSON, formato
comum na atualidade e que pode ser importado, muitas vezes
nativamente, na maioria das linguagens de programação modernas. Assim,
sendo possível utilizar estes mesmos dados em outras linguagens de
programação.

Neste documento estaremos utilizando o deck DECOMP CCEE
[*DC201805.zip*](http://www.ccee.org.br/ccee/documentos/DC201805) que
consiste do deck do CMO de Maio/2018;

## Instalação do módulo Python

A principal dependência para a instalação é o Python 3.6.x instalado
(no Ubuntu/Linux pacotes python3 e python3-venv). Também será
necessário o comando *git* para a instalação facilitada do módulo
Python. No exemplo apresentado neste documento foi utilizado o sistema
operacional Linux mas o Windows também é suportado. Ao executar o
comando *python3.6* no terminal teremos o apresentado abaixo, variando
com a versão instalada no seu sistema.

```
$ python3.6
Python 3.6.5 (default, May  3 2018, 10:08:28)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Para criar o ambiente virtual de execução e instalar o módulo do
importador será necessário executar os comandos abaixo:

```
$ python3.6 -m venv --prompt='Importador' venv-3.6
$ source venv-3.6/bin/activate
(Importador) $ pip install --upgrade pip setuptools
Collecting pip
  Using cached https://files.pythonhosted.org/packages/43/84/23ed6a1796480a6f1a2d38f2802901d078266bda38388954d01d3f2e821d/pip-20.1.1-py2.py3-none-any.whl
Collecting setuptools
  Downloading https://files.pythonhosted.org/packages/c4/f9/15ec4639c50f54043a6d385a89447f69b3ee3601f65cc7c17ab8c178f0a6/setuptools-47.3.0-py3-none-any.whl (583kB)
    100% |████████████████████████████████| 583kB 2.2MB/s
Installing collected packages: pip, setuptools
  Found existing installation: pip 9.0.3
    Uninstalling pip-9.0.3:
      Successfully uninstalled pip-9.0.3
  Found existing installation: setuptools 39.2.0
    Uninstalling setuptools-39.2.0:
      Successfully uninstalled setuptools-39.2.0
Successfully installed pip-20.1.1 setuptools-47.3.0
(Importador) $ pip install git+https://git@github.com/venidera/deckparser.git
Collecting git+https://****@github.com/venidera/deckparser.git
  Cloning https://****@github.com/venidera/deckparser.git to /tmp/pip-req-build-am1e89ag
  Running command git clone -q 'https://****@github.com/venidera/deckparser.git' /tmp/pip-req-build-am1e89ag
Collecting numpy
  Using cached numpy-1.18.5-cp36-cp36m-manylinux1_x86_64.whl (20.1 MB)
Collecting unidecode
  Using cached Unidecode-1.1.1-py2.py3-none-any.whl (238 kB)
Collecting chardet
  Using cached chardet-3.0.4-py2.py3-none-any.whl (133 kB)
Using legacy setup.py install for deckparser, since package 'wheel' is not installed.
Installing collected packages: numpy, unidecode, chardet, deckparser
    Running setup.py install for deckparser ... done
Successfully installed chardet-3.0.4 deckparser-1.0.1 numpy-1.18.5 unidecode-1.1.1
```

Nesta instalação está sendo utilizado um *virtualenv* Python para
instalação dos pacotes. A desativação deste *virtualenv* pode ser
realizada executando o comando *deactivate*. O comando *source
venv-3.6/bin/activate* ativa o *virtualenv*. A utilização do pacote do
importador exigirá a ativação do ambiente virtual onde ele foi
instalado.

## Extraindo dados para formato JSON

A forma mais simples de testar a instalação e o importador, é extrair
os dados utilizando o comando *decomp2json*, que possui a sintaxe
abaixo:

```
$ decomp2json
Conversor do deck de dados do DECOMP para formato JSON
Sintaxe: decomp2json <deck-file-path> [semana [registro]]
Semana: Número da semana (revisões), começando por 1
Registros: UH, CT, UE, DP, PQ, IT, IA, TX, DT, MP, VE, VM, DF, TI, MT, VI, RE, AC
Exemplos:
decomp2json DC201805.zip
decomp2json DC201805.zip 2
decomp2json DC201805.zip 1 UE
decomp2json DC201805.zip > DC201805.json
```

Por exemplo, a saída para a extração dos registro UE da (estações de
bombeamento), na primeira semana (revisão 0) fica:

```
$ decomp2json DC201805.zip 1 UE
INFO:root:invalid literal for int() with base 10: '' linha: 3020
[
 {
  "VazMax": 160.0,
  "Nome": "Sta Cecilia",
  "Montante": 125,
  "VazMin": 75.0,
  "Consumo": 0.2,
  "Jusante": 181
 },
 {
  "VazMax": 190.0,
  "Nome": "Vigario",
  "Montante": 181,
  "VazMin": 75.0,
  "Consumo": 0.44,
  "Jusante": 182
 },
 {
  "VazMax": 270.0,
  "Nome": "Traicao",
  "Montante": 108,
  "VazMin": 0.0,
  "Consumo": 0.3,
  "Jusante": 109
 },
 {
  "VazMax": 395.0,
  "Nome": "Pedreira",
  "Montante": 109,
  "VazMin": 0.0,
  "Consumo": 0.25,
  "Jusante": 118
 }
]
```

Note que o comando aponta um erro existente no formato do arquivo do
DECOMP na linha 3020 do arquivo DADGER no registro UE.

## Estrutura do importador

O importador foi implementado através de algumas classes e funções que
realizam atividades específicas. São elas:

* *DecompZipped*: é a classe que realiza a abertura do arquivo zipado
  do deck DECOMP, possuindo rotinas para abrir cada revisão semanal, e
  extração dos arquivos associados.

* Importadores: os importadores são as funções específicas para cada
  arquivo importado de uma revisão do deck DECOMP::
  + importDADGER: Importa arquivo DADGER.XXX, de dados gerais de
    planejamento, composto por blocos de dados, onde cada bloco é
    composto por registros formatados. O importador permite extrair os
    seguintes registros:
	- UH (usinas hidrelétricas),
	- CT (usinas termoelétricas),
	- UE (estações de bombeamento),
	- DP (carga dos subsistemas),
	- PQ (geração em pequenas usinas),
	- IT (restrição de geração de itaipu 50Hz e carga da ANDE),
	- IA (limite de fluxo entre subsistemas)
	- TX (taxa de desconto anual)
	- DT (data de referência do estudo)
	- MP e MT (manutenção programada)
	- VE (volume de espera)
	- VM e DF (enchimento de volume morto)
	- TI (taxa de irrigação)
	- VI (tempo de viagem)
	- RE, LU, FU, FT e FI (restrições elétricas)
	- AC (modificação de cadastro)
  + importVAZOES: Importa arquivo VAZOES.XXX, de dados de afluência
    (vazão incremental para cada aproveitamento) que compões a
    previsão do mês inicial e os cenários de vazões para cada estágio
    do planejamento (gerado pelo GEVAZP). O arquivo possui um cenário
    para cada estágio (semana) do primeiro mês, e diversos cenários
    para o segundo mês. São extraídos os dados de vazão para cada
    estágio do mês inicial.

Todo o código do importador é aberto e está disponível no endereço
[https://github.com/venidera/deckparser](https://github.com/venidera/deckparser)
sob licença Apache v2. Os arquivos e registros importados são os de
interesse do modelo ODIN-S até o momento.

## Executando a importação

Os importadores podem ser utilizados de maneira isolada, ou juntos
através da função *decomp2dicts*.

A importação isolada de um arquivo está demostrada nos próximos 3
exemplos abaixo.

Primeiro, é realizada a importação do registro IT do arquivo
*DADGER.XXX* da primeira semana:


```
>>> from deckparser.decompzipped import DecompZipped
>>> from deckparser.importers.decomp.importDADGER import importDADGER
>>>
>>> dz = DecompZipped('DC201805.zip')
>>> it = importDADGER(dz.openFileExtData(1,'DADGER'),'IT')
>>> it
[{'Mande': [66.0, 3769.0, 3418.0], 'Estagio': 1, 'GerIt50': [66.0, 3769.0, 3418.0]}, {'Mande': [66.0, 3719.0, 3368.0], 'Estagio': 6, 'GerIt50': [66.0, 3719.0, 3368.0]}]
```

Abaixo segue um exemplo da importação completa do arquivo *DADGER.XXX*
da primeira semana:

```
>>> dadger=importDADGER(dz.openFileExtData(1,'DADGER'))
>>> dadger
{'VI': [{'Duracao': 360, 'VazDef': [80.0, 87.0, 88.0, 81.0, 81.0], 'CodUhe': 156}, {'Duracao': 360, 'VazDef': [25.0, 15.0, 10.0, 10.0, 10.0], 'CodUhe': 162}], 'AC': [{'CodUhe': 285, 'Valor': 72.71, 'Mnemonico': 'JUSMED', 'Estagio': 1, 'Mes': 'MAI'}, {'CodUhe': 285, 'Valor': 72.71, 'Mnemonico': 'JUSMED', 'Estagio': 2, 'Mes': 'MAI'}, {'CodUhe': 285, 'Valor': 72.71, 'Mnemonico': 'JUSMED', 'Estagio': 3, 'Mes': 'MAI'}, {'CodUhe': 285, 'Valor': 72.71, 'Mnemonico': 'JUSMED', 'Estagio': 4, 'Mes': 'MAI'}, {'CodUhe': 285, 'Valor': 72.71, 'Mnemonico': 'JUSMED', 'Estagio': 5, 'Mes': 'MAI'}, {'CodUhe': 285, 'Valor': 70.71, 'Mnemonico': 'JUSMED'...
```

Por fim, um exemplo da importação das vazões previstas da segunda revisão:

```
>>> from deckparser.importers.decomp.importVAZOES import importVAZOES
>>> from deckparser.importers.newave.importHIDR import importHIDR
>>> HIDR, HIDRcount = importHIDR(fn=dz.extractFile(2,'HIDR'))
>>> HIDRcount
320
>>> vaz = importVAZOES(fn=dz.extractFile(2,'VAZOES'),blockSize=HIDRcount)
>>> vaz
{'numEstagios': 5, 'numDiasExcl': 1, 'semanasCompletas': 4, 'mesIni': 5, 'numPostos': 157, 'anoIni': 2018, 'aberturas': [1, 1, 1, 1, 267], 'prevSem': [[46, 0, 0, 0, 0, 139, 57, 13, 5, 15, 34, 96, 0, 20, 13, 0, 201, 186, 0, 0, 0, 56, 22, 119, 136, 0, 0, 2, 0, 0, 143, 71, 692, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 137, 3, 70, 110, 9, 18, 0, 0, 0, 0, 116, 0, 0, 0, 283, 50, 116, 0, 0, 0, 0, 0, 0, 0, 37, 2, 6, 237, 0, 42, 42, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0...

```

Note que para importar as vazões, é necessário saber o tamanho do
bloco do arquivo HIDR.DAT (número de registros). Para isto e utilizado
o módulo provindo do importador do NEWAVE.

A importação completa do deck do DECOMP, incluindo todas as revisões,
pode ser realizada através da função *decomp2dicts*

```
>>> from deckparser.decomp2dicts import decomp2dicts
>>> deck = decomp2dicts('DC201805.zip')
>>> deck
[{'DADGER': {'VI': [{'CodUhe': 156, 'Duracao': 360, 'VazDef': [80.0, 87.0, 88.0, 81.0, 81.0]}, {'CodUhe': 162, 'Duracao': 360, 'VazDef': [25.0, 15.0, 10.0, 10.0, 10.0]}], 'DF': [], 'DT': {'Ano': 2018, 'Mes': 4, 'Dia': 28}, 'DP': [{'MMED': [45318.0, 41626.0, 32270.0], 'Estagio': 1, 'NumPatamares': 3, 'CodSubsistema': 1...
```


## Atualizações

O processo de importação segue em atualização visto que o modelo
DECOMP está evolução contínua. Assim, sempre que necessário ou que um
novo dado é adicionado o importador é atualizado para contemplar o
dado na importação caso seja de interesse para uso no modelo ODIN-S.
