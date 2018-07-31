# Processo de Importação de Decks NEWAVE

Neste documento são apresentados os procedimentos, arquivos importados e sugestões de uso para os dados obtidos através dos decks do modelo NEWAVE produzido pelo CEPEL.

Basicamente, o importador realiza a aquisição dos dados contidos em um deck NEWAVE e os converte para objetos na linguagem Python. Após o processo os dados podem ser acessados facilmente e podem ser realizadas as utilizações que os usuários desejarem tais como a implementação de programas ou ainda a exportação para formatos mais amigáveis como os *csv* e *xls/xlsx*, entre outros formatos transacionais como JSON e XML.

Serão utilizados dois decks NEWAVE distintos para apresentação:

1. Deck NEWAVE CCEE - [*NW201807.zip*](http://www.ccee.org.br/ccee/documentos/NW201807) que consiste do deck de PMO de Julho/2018;

2. Deck PDE 2026 EPE - [*PDE2026 Referencia.zip*](http://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-40/topico-67/PDE2026%20Referencia.zip) que consiste do deck de planejamento do PDE 2026.

Cada deck tem particularidades e serão apresentadas algumas comparações relativas a cada deck.

## Instalação do módulo Python

A principal dependência para a instalação é o Python 3.6.x instalado. Também será necessário o comando *git* para a instalação facilitada do módulo Python. No exemplo apresentado neste documento foi utilizado o sistema operacional Linux mas o Windows também é suportado. Ao executar o comando *python3.5* no terminal teremos o apresentado abaixo, variando com a versão instalada no seu sistema.

```
$ python3.6
Python 3.6.5 (default, May  3 2018, 10:08:28)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Para criar o ambiente virtual de execução e instalar o módulo do importador será necessário executar os comandos abaixo:

```
$ python3.6 -m venv --prompt='Importador' venv-3.6 --without-pip
$ source venv-3.6/bin/activate
(Importador) $ wget https://bootstrap.pypa.io/get-pip.py
--2018-07-31 15:07:20--  https://bootstrap.pypa.io/get-pip.py
Resolving bootstrap.pypa.io (bootstrap.pypa.io)... 151.101.92.175, 2a04:4e42:16::175
Connecting to bootstrap.pypa.io (bootstrap.pypa.io)|151.101.92.175|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1642522 (1.6M) [text/x-python]
Saving to: ‘get-pip.py’

get-pip.py                             100%[====================>]   1.57M  2.05MB/s    in 0.8s

2018-07-31 15:07:21 (2.05 MB/s) - ‘get-pip.py’ saved [1642522/1642522]
(Importador) $ python get-pip.py && rm -fr get-pip.py
Collecting pip
  Downloading https://files.pythonhosted.org/packages/5f/25/e52d3f31441505a5f3af41213346e5b6c221c9e086a166f3703d2ddaf940/pip-18.0-py2.py3-none-any.whl (1.3MB)
    100% |████████████████████████████████| 1.3MB 2.7MB/s
Collecting setuptools
  Downloading https://files.pythonhosted.org/packages/ff/f4/385715ccc461885f3cedf57a41ae3c12b5fec3f35cce4c8706b1a112a133/setuptools-40.0.0-py2.py3-none-any.whl (567kB)
    100% |████████████████████████████████| 573kB 4.8MB/s
Collecting wheel
  Downloading https://files.pythonhosted.org/packages/81/30/e935244ca6165187ae8be876b6316ae201b71485538ffac1d718843025a9/wheel-0.31.1-py2.py3-none-any.whl (41kB)
    100% |████████████████████████████████| 51kB 4.8MB/s
Installing collected packages: pip, setuptools, wheel
Successfully installed pip-18.0 setuptools-40.0.0 wheel-0.31.1
(Importador) $ pip install pip setuptools --upgrade
Requirement already up-to-date: pip in ./venv-3.6/lib/python3.6/site-packages (18.0)
Requirement already up-to-date: setuptools in ./venv-3.6/lib/python3.6/site-packages (40.0.0)
(Importador) $ pip install git+https://git@github.com/venidera/deckparser.git
Collecting git+https://git@github.com/venidera/deckparser.git
  Cloning https://git@github.com/venidera/deckparser.git to /tmp/pip-req-build-s31se6m8
Collecting numpy (from deckparser==0.0.1)
  Downloading https://files.pythonhosted.org/packages/88/29/f4c845648ed23264e986cdc5fbab5f8eace1be5e62144ef69ccc7189461d/numpy-1.15.0-cp36-cp36m-manylinux1_x86_64.whl (13.9MB)
    100% |████████████████████████████████| 13.9MB 1.6MB/s
Collecting unidecode (from deckparser==0.0.1)
  Downloading https://files.pythonhosted.org/packages/59/ef/67085e30e8bbcdd76e2f0a4ad8151c13a2c5bce77c85f8cad6e1f16fb141/Unidecode-1.0.22-py2.py3-none-any.whl (235kB)
    100% |████████████████████████████████| 235kB 6.2MB/s
Building wheels for collected packages: deckparser
  Running setup.py bdist_wheel for deckparser ... done
  Stored in directory: /tmp/pip-ephem-wheel-cache-ultpz0sm/wheels/7b/dc/81/f714e8db04092b1d6ebe790dcc613ab906c88d2cf10715dc8a
Successfully built deckparser
Installing collected packages: numpy, unidecode, deckparser
Successfully installed deckparser-0.0.1 numpy-1.15.0 unidecode-1.0.22
```

O teste do procedimento pode ser feito fazendo o import do módulo do importador executando:

```
(Importador) $ python
Python 3.6.5 (default, May  3 2018, 10:08:28)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import deckparser
>>>
```

Nesta instalação está sendo utilizado um *virtualenv* Python para instalação dos pacotes. A desativação deste *virtualenv* pode ser realizada executando o comando *deactivate*. O comando *source venv-3.6/bin/activate* ativa o *virtualenv*. A utilização do pacote do importador exigirá a ativação do ambiente virtual onde ele foi instalado.

## Estrutura do importador

O importador foi implementado através de algumas classes e funções que realizam atividades específicas. São elas:

* *NewaveZipped*: é a classe que realiza a abertura do arquivo zipado do deck e verifica se este possui os arquivos de um deck NEWAVE. Caso existam decks zipados dentro do arquivo indicado, o arquivo comprimido de data mais recente será o selecionado independentemente do nível de encapsulamento de arquivos comprimidos uns dentro dos outros.

* *NewaveDicted*: trata-se de uma classe template (interface) para agrupar os dados importados. Esta classe pode ser utilizada para implementar métodos que farão uso dos dados.

* Importadores: os importadores são as funções específicas para cada arquivo importado do deck NEWAVE, são importados os arquivos:
    + DGER: mantém a configuração do estudo executado no NEWAVE;
    + SISTEMA: contém as informações de patamares de déficit, custos de déficit, limites de intercâmbio, mercado de energia total, geração de pequenas usinas, e informações de máximo recebimento/fornecimento;
    + PATAMAR: número de patamares, duração mensal dos patamares, carga e intercâmbio para os patamares;
    + CAR: curva de aversão a risco;
    + C_ADIC: carga adicional que pode ser adicionada aos subsistemas;
    + TERM: base de dados do parque termelétrico;
    + CADTERM: informações adicionais para as usinas termelétricas. Este arquivo não está presente no deck PDE;
    + EXPT: arquivo que descreve a expansão do parque termelétrico;
    + CONFT: arquivo que define a participação e o estado das usinas termelétricas no estudo executado pelo NEWAVE;
    + CLAST: arquivo que apresenta as informações de custo para as classes de termelétricas. Também mantém os dados de alteração de preços no tempo;
    + MANUTT: mantém as informações de manutenção do parque termelétrico;
    + HIDR: base de dados do parque hidrelétrico;
    + CONFHD: arquivo que define a participação e o estado das usinas hidrelétricas no estudo executado pelo NEWAVE;
    + MODIF: arquivo que realiza alterações nas restrições operativas das usinas na execução do NEWAVE;
    + DSVAGUA: arquivo que define usos múltiplos para a água dos reservatórios e também vazões remanescentes;
    + VAZOES: arquivo que mantém o histórico de vazões afluentes aos reservatórios das hidrelétricas do sistema;
    + EXPH: arquivo que mantém os dados de expansão do parque hidrelétrico indicando os enchimentos de volume morto e a motorização das usinas;

As extensões dos arquivos variam de acordo para cada deck sendo importante manter os nomes dos arquivos. Por exemplo, o arquivo *dger.dat* é encontrado no deck de PMO e no deck de PDE (2026) o equivalente é o *dger.d26*.

Todo o código do importador é aberto e está disponível no endereço [https://github.com/venidera/deckparser](https://github.com/venidera/deckparser) sob licença Apache v2.

## Executando a importação

Os importadores podem ser utilizados de maneira isolada. Visando acelerar o processo foi construída uma função denominada *newave2dicts* que realiza toda a importação dos arquivos listados acima.

A importação isolada de um arquivo está demostrada abaixo. No exemplo é realizada a importação do arquivo *SISTEMA.DAT*, e para isso é necessário importador o arquivo *DGER.DAT*:


```
>>> from deckparser.deckzipped import DeckZipped
>>> from deckparser.importers.newave.importDGER import importDGER
>>> from deckparser.importers.newave.importSISTEMA import importSISTEMA
>>>
>>> dz = DeckZipped('PDE2026 Referencia.zip')
>>> dger = importDGER(dz.openFile(fnp='dger'))
>>> SISTEMA = importSISTEMA(dz.openFileExtData(fnp='sistema'), dger)
>>> dger
{'info': 'PLANO DECENAL DE EXPANSAO DA GERACAO 2026 - EPE - Janeiro/2017', 'tipoexec': ...
>>> SISTEMA
SISTEMA
{'npdef': 1, 'sss': {'10': {'name': 'PARANA', 'fict': 0}, '1': {'name': 'SUDESTE', 'fict': 0}, '2': {'name': 'SUL', 'fict': 0}, '3': {'name': 'NORDESTE', 'fict': 0}, '4': {'name': 'NORTE', 'fict': 0}, '5': {'name': 'ITAIPU', 'fict': 0}, '6': {'name': 'AC RO', 'fict': 0}, '7': {'name': 'MAN AP BV', 'fict': 0}, '8': {'name': 'B.MONTE', 'fict': 0}, '9': {'name': 'T. PIRES', 'fict': 0}, '11': {'name': 'TAPAJOS', 'fict': 0}, '100': {'name': 'IVAIPORA', 'fict': 1}, '200': {'name': 'IMPERATRIZ', 'fict': 1}, '300': {'name': 'XINGU', 'fict': 1}}, 'deficit': {'10': {}, '1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}, '9': {}, '11': {}, 10: {'defpat1': '4650.00', 'defpat2': '0.00', 'defpat3': '0.00', 'defpat4': '0.00', 'pucortepat1': '1.000', 'pucortepat2': '0.000', 'pucortepat3': '0.000', 'pucortepat4': '0.000'}}, 'liminter': [{'ORI': '1', 'DES': '2', 'limites': [3665.0, 3665.0, 3665.0, 3665.0, 3665.0, 3665.0, 3665.0, 3665.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307.0, 4307. ...
```

Abaixo é apresentado o código da função *newave2dicts* que faz a importação completa de um deck NEWAVE para um objeto da classes *NewaveDicted* que basicamente é um objeto que agrega todos os dados como sendo um tipo de pacote. Os arquivos importados são os de interesse do modelo ODIN até o momento.

```
def newave2dicts(fn):
    dz = NewaveZipped(fn=fn)
    if dz.zipLoaded():
        dd = NewaveDicted()
        dd.dirname = dz.dirname
        dd.filename = dz.filename
        dd.fhash = dz.fhash
        dd.DGER = importDGER(dz.openFile(fnp='dger'))
        dd.SISTEMA = importSISTEMA(dz.openFileExtData(fnp='sistema'), dd.DGER)
        dd.process_ss()
        dd.PATDURA, dd.PATCARGA, dd.PATINTER, dd.np = importPATAMAR(dz.openFileExtData(fnp='patamar'), dd.DGER, dd.sss)
        dd.CAR = importCAR(dz.openFileExtData(fnp='curva'), dd.DGER)
        dd.CADIC = importCADIC(dz.openFileExtData(fnp='c_adic'), dd.DGER)
        dd.TERM = importTERM(dz.openFile(fnp='term'))
        dd.CADTERM = importCADTERM(dz.openFile(fnp='cadterm'))
        dd.EXPT = importEXPT(fobj=dz.openFile(fnp='expt'), utes=dd.TERM.keys())
        dd.CONFT = importCONFT(dz.openFile(fnp='conft'))
        dd.CLAST, dd.MODIFCLAST = importCLAST(fobj=dz.openFile(fnp='clast'), utes=dd.TERM.keys(), nyears=len(dd.DGER['yph']))
        dd.MANUTT = importMANUTT(fobj=dz.openFile(fnp='manutt'), utes=dd.TERM.keys())
        dd.HIDR, dd.HIDRcount = importHIDR(fn=dz.extractFile(fnp='hidr'))
        dd.CONFHD = importCONFHD(dz.openFile(fnp='confhd'))
        dd.MODIF = importMODIF(fobj=dz.openFile(fnp='modif'), uhes=dd.CONFHD.keys())
        dd.DSVAGUA = importDSVAGUA(dz.openFileExtData(fnp='dsvagua'), uhes=dd.CONFHD.keys(), dger=dd.DGER)
        dd.VAZOES, dd.VAZcount, dd.vaz = importVAZOES(fn=dz.extractFile(fnp='vazoes'), hcount=dd.HIDRcount, dger=dd.DGER)
        dd.ENCHVM, dd.MOTORI = importEXPH(dz.openFileExtData(fnp='exph'))
        dd.SHISTANO = importSHIST(dz.openFileExtData(fnp='shist'))
        return dd
    else:
        return None
````

A execução de uma importação completa é realizada como apresentado abaixo:

```
>>> from deckparser.newave2dicts import newave2dicts
>>> pde = newave2dicts('PDE2026 Referencia.zip')
>>> pde
<deckparser.newavedicted.NewaveDicted object at 0x111da7c50>
>>> dir(pde)
['CADIC', 'CADTERM', 'CAR', 'CLAST', 'CONFHD', 'CONFT', 'DGER', 'DSVAGUA', 'ENCHVM', 'EXPT', 'HIDR', 'HIDRcount', 'MANUTT', 'MODIF', 'MODIFCLAST', 'MOTORI', 'PATCARGA', 'PATDURA', 'PATINTER', 'SHISTANO', 'SISTEMA', 'TERM', 'VAZMAX', 'VAZOES', 'VAZcount', ... , 'dirname', 'fhash', 'filename', 'np', 'nss', 'process_ss', 'ssfict', 'ssname', 'sss', 'vaz']
```

Como podemos verificar acima, os arquivos foram convertidos em proriedades do objeto *NewaveDicted*. Com este objeto criado podemos fazer acesso aos dados de forma indexada, o que agiliza os processos de uso dos dados disponíveis no deck.

Acima foram apresentados alguns dados dos arquivos *DGER* e *SISTEMA* e abaixo apresentamos exemplos de acessos a outros dados:

```
>>> pde.SISTEMA['sss']['1']
{'name': 'SUDESTE', 'fict': 0}
>>> pde.SISTEMA['mercado']['1']
{'demanda': [35929.0, 35121.0, 35380.0, 36398.0, 36834.0 ...
>>> pde.HIDR['CAMARGOS']['ProdEspec']
0.0085249999538064
>>> pde.CONFT['1']
{'nome': 'ANGRA 1', 'ssis': '1', 'exis': 'EE', 'classe': '1'}
>>> pde.CONFHD['1']
{'nome': 'CAMARGOS', 'posto': '1', 'jus': '2', 'ssis': '10', 'vinic': '74.82', 'uexis': 'EX', 'modif': '0', 'inihist': '1931', 'fimhist': '2014'}
```

Como apresentado acima, temos a verificação de qual o nome do subsistema de código 1 que é o SUDESTE, é apresentado um exemplo do mercado de energia do subsistema SUDESTE. É apresentada a Produtibilidade Específica da UHE de CAMARGOS e o código dela no estudo (Código 1).

## Usos para os dados importados

Os usos para os dados importados são múltiplos. Como mencionado anteriormente, para programadores Python, os dados poderão ser utilizados para submissão como entrada em modelos de simulação e otimização e também podem ser exportados para formatos mais amigáveis ou transacionais. Apresentamos abaixo a exportação dos dados para um arquivo em format JSON, formato comum na atualidade e que pode ser importado, muitas vezes nativamente, na maioria das linguagens de programação modernas, assim, seria possível utilizar estes mesmos dados em outras linguagens de programação.

```
>>> from json import dumps
>>> with open('deck.json', 'w+') as f:
...    f.write(dumps(pde.__dict__))
>>>
```

Acima foi criado o arquivo *deck.json* que armazena o todo o deck seguindo a estrutura do objeto. A importação destes dados no Python pode ser feita com o código abaixo:

```
>>> from json import loads
>>> pde = loads(open('deck.json').read())
>>>
```

## Atualizações

O processo de importação segue em atualização visto que o modelo NEWAVE está evolução contínua, assim, sempre que necessário ou que um novo dado é adicionado o importador é atualizado para contemplar o dado na importação caso seja de interesse para uso no modelo ODIN.