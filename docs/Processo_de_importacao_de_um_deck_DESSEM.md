# Importação de Decks DESSEM

Neste documento são apresentados os procedimentos, arquivos importados
e sugestões de uso para os dados obtidos através dos decks do modelo
DESSEM produzido pelo CEPEL.

O importador consiste numa biblioteca que realiza a extração dos dados
contidos em um deck DESSEM e os converte para objetos na linguagem
Python, que podem ser utilizados para submissão como entrada em
modelos de simulação e otimização, e também podem ser exportados para
formatos mais amigáveis ou transacionais.

Neste documento estaremos utilizando o conjunto de decks DESSEM CCEE
(https://www.ccee.org.br/ccee/documentos/CCEE_640604) [*DES_201805.zip*]
que consiste dos decks do PMO de maio/2018;

## Instalação do módulo Python

...

## Estrutura do importador

O importador dos decks do DESSEM está localizado no pactote "deckparser.importers.dessem", 
que possui os seguintes pacotoes:

- Pacote "cfg": contém os arquivos de configuração, em formato xml, que determina 
a estrutura dos dados contidos em cada arquivo do deck. Cada arquivo xml contém:

	- Atributo "name": nome de identificação do tipo de arquivo;
	- Conjunto de elementos tipo "record" e/ou "table", cada um contendo:
		- Atributo "name": nome do registro;
		- Conjunto de elementos tipo "field", que identificam cada campo do registro, 
			contendo:
			- Atributos: nome (name), tipo de dado (type), valor default (default) e 
				valores especiais (special)
			- Elemento com validações (validation), 
			- Estrutura de campos compostos (composed=True).

- Pacote "core": cotém os módulos que realizam os métodos fundamentais utilizados 
na importação, as principais classes destes módulos são:

	- xmlReader: responsável por fazer a leitura dos arquivos de configuração;
	- record: classe que representa a estrutura de dados de cada registro dos arquivos do deck.
		É responsável por fazer a leitura de todos os campos;
	- table: realiza a leitura dos resgitros múltiplos e armzena os dados lidos em uma lista;
	- dsFile: classe abstrata que é estendida pelas classes importadoras, que por sua vez 
		realizam a importação dos dados de cada arquivo do deck. A função desta classe é fazer a 
		leitura de todos os registros do arquivo;
		O pacote "core" ainda contém o módulo "dataType.py", que contém métodos para decodificar
		e validar cada tipo de dado.

O arquivo "hidr", por ser um arquivo não formatado (codificado), possui metodologia de 
leitura especifica, mas semelhante à leitura dos demais arquivos.

** Cada módulo localizado no pacote "dessem" contém uma classe que realiza a importação 
de um arquivo específico. O conjunto de arquivos que podem ser lidos é:

- Arquivos de indice:
	- "dessem": índice para a leitura dos demais arquivos
	- "desselet": dados sobre os intervalos de tempo e índice dos arquivos que contém os dados
		da rede elétrica em cada caso base (patamar de carga) e as alterações de rede elétrica 
		aplicadas especificamente para cada intervalo de tempo;

- Arquivo com dados gerais do caso:
	- "entdados": dados diversos sobre cada elemento do sistema, além de dados sobre a 
		configuração dos intervalos de tempo, entre outras opções de configuração do estudo;

- Arquivos com dados das usinas hidrelétricas, rede hidráulica e restrições aplicáveis:
	- "hidr":  dados cadastrais e construtivos das usinas hidrelétricas;
	- "operuh": dados sobre as restrições de operação hidraúlica;
	- "dadvaz": dados sobre as vazões naturais afluentes ao longo do período de interesse;
	- "curvtviag": dados sobre a propagação da água entre usinas hidrelétricas;
	- "cotasr11": dados para obtenção da cota da régua 11;
	- "ils_tri": dados sobre a operação do canal Pereira Barreto 
		(entre as usinas de Ilha Solteira e Três Irmãos);
		
- Arquivos com dados para simulação (período de pré-interesse):
	- "simul": dados sobre a simulação hidráulica anterior ao período de interesse;
	- "deflant": dados sobre as vazões defluentes anteriores ao início do período de interesse;

- Arquivos com dados sobre área de controle e reserva de potência:
	- "areacont": dados das áreas de controle;
	- "respot": dados sobre reserva de potência mínima;

- Arquivos com dados da rede elétrica:
	- "eletbase": dados básicos da rede elétrica para cada caso (patamar de carga);
	- "eletmodif": dados sobre as modificações da rede elétrica aplicadas em cada 
		intervalo de tempo;

- Arquivos com dados das usinas termelétricas:
	- "termdat": dados cadastrais das usinas termelétricas;
	- "operut": dados sobre a operação termelétrica, incluindo restrições;
	- "ptoper": dados sobre a operação de usinas que não são decididos pelo modelo DESSEM
		(atualmente somente a leitura dos dados sobre a geração termelétrica antecipada 
		está configurada);

- Outros arquivos:
	- "infofcf": dados sobre a função de custo futuro do DECOMP;
	- "tolperd": dados sobre a tolerência para convergência do valor das perdas elétricas;

- Arquivos sem leitura (codificados):
	- "mlt": dados sobre média de longo termo das vazões naturais afluentes;
	- "mapcut": dados sobre a função de custo futuro do DECOMP;

O módulo "util" contém alguns métodos destinados a realizar testes.
O módulo "teste" contém exemplos de testes. 

## Executando a importação

A importação dos dados em objetos do tipo "dict" é realizada utilizando o método 
"desssem2dicts", a sintaxe deste é método é a seguinte:

>>>> from deckparser.dessem2dicts import dessem2dicts
>>>> dc = desssem2dicts(fn, dia, rd)

Onde:

fn: é o caminho para o arquivo compactado que contém os decks do DESSEM

dia: especifica os dias que deverão ser lidos, pode ser:
	- datetime.date(Y,m,d);
	- list contendo objetos do tipo datetime.date;
	- None (todos os dias encontrados no arquivo)

rd: especifica se devem ser lidos os casos com rede (True), sem rede (False) 
ou ambos ("None" ou [True,False])

** O arquivo (compactado) fornecido deve conter arquivos também compactados (casos), 
cada um destes contendo os arquivos do deck. Cada arquivo (caso) deve possuir nome  
conforme o padrao:

DES_CCEE_(yyyy)(mm)(dd)_(Com|Sem)Rede.zip

Onde:
yyyy, mm, dd: são ano, mês e dia do caso;
Com (Sem): indica se o caso considera (ou não) a rede elétrica.

** Pode-se escolher o padrão dos nomes de arquivo utilizando o quarto argumento do 
método desssem2dicts:

>>>> dc = desssem2dicts(fn, dia, rd, {'file_pattern':2})

O padrão acima mencionado correponde à opção file_pattern=1.
O formato para file_pattern=2 é:

DS_CCEE_(mm)(yyyy)_(COM|SEM)REDE_RV(r)D(dd).zip

Onde:
yyyy, mm, dd: são ano, mês e dia do caso;
r: é a revisão do PMO 
COM (SEM): indica se o caso considera (ou não) a rede elétrica.

** O resultado da leitura é o um objeto "dict" com a seguinte estrutura:

{dia: {r: caso:dict}}

Onde:
dia: é um objeto do tipo date
r: indica se o caso considera rede elétrica (bool)
(ex.: {date(2018,05,25): {True: casoComRede, False: casoSemRede}})

O conjunto de dados de cada caso possui a seguinte estrutura:

{arquivo: {(registro|tabela): (dados:(dict|list))}
(ex.: {'entdados': {'UH': dados, ...}})

O conjunto de dados de cada registro é estruturado na forma: {campo: valor}
(ex.: {'idUsina': 66, 'nomeUsina': 'ITAIPU', ...})

Caso o resgitro seja múltiplo (tabela), os dados são fornecidos em um objeto do tipo "list", 
contendo um objeto "dict" (conforme estrutura do registro) para cada registro lido.

Os dados do arquivo "hidr" são estruturados em uma única tabela: {'hidr': (tabela:list)}.

** A classe Loader é responsável por realizar o carregamento dos dados de um deck. 
O código abaixo realiza a leitura do caso contido no diretório "dr" e armazena 
o resultado da leitura em "dc":

>>> from deckparser.importers.dessem.loader import Loader
>>> from datetime import date
>>> 
>>> ld = Loader(dr)
>>> ld.loadAll()
>>> dc = ld.toDict()

## Atualizações

O processo de importação segue em atualização visto que o modelo
DESSEM está em evolução contínua. Assim, sempre que necessário ou que um
novo dado é adicionado o importador é atualizado para contemplar o
dado na importação caso seja de interesse para uso no modelo ODIN-H.
