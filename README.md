DeckParser: Um leitor de dados do NEWAVE, DECOMP and DESSEM
=============================================

![GitHub Release](https://img.shields.io/badge/release-v0.0.1-blue.svg)
![GitHub license](https://img.shields.io/badge/license-Apachev2-yellow.svg)

DeckParser fornece programas para abrir e ler os dados dos programas NEWAVE, DECOMP e DESSEM

* Projeto em desenvolvimento - não aberto ainda para contribuições da comunidade (pull requests)

## Dependências

* Python > 3.6.x
* numpy > 1.15.x (Instalado automaticamente)
* unidecode > 1.0.x (Instalado automaticamente)

## Validações

### Leituras

* DGER.DAT: validado para todos os decks NEWAVE da CCEE;
* SISTEMA.DAT: validado para todos os decks NEWAVE da CCEE.

### Considerações

* Quando um deck é um arquivo zipado com mais de um deck dentro, o arquivo mais novo de deck encontrado no arquivo comprimido é o utilizado para a importação.

## Uso

* Exemplo 1: ler arquivo `SISTEMA.DAT`:

```python
from deckparser.deckzipped import DeckZipped
from deckparser.importers.newave.importDGER import importDGER
from deckparser.importers.newave.importSISTEMA import importSISTEMA

dz = DeckZipped('/Users/andre/git/deckparser/test/NW201305.zip')
dger = importDGER(dz.openFile(fnp='dger'))
SISTEMA = importSISTEMA(dz.openFileExtData(fnp='sistema'), dger)
```

* Example 2: ler deck do newave dentro de um `dict`:

```python
from deckparser.newave2dicts import newave2dicts
deck = newave2dicts('/Users/andre/git/deckparser/test/NW201305.zip')
```

## Instalação

Usando pip:

```bash
$ pip install git+https://git@github.com/venidera/deckparser.git
```

## Patrocinador

![](./imgs/logo_ped_aneel.jpg?raw=true)

"Este trabalho faz parte do projeto intitulado 'Análise de Portfólio de Usinas de Geração para Atendimento da Carga Futura do Sistema Interligado Nacional - Matriz Robusta’, financiado pela EDP no âmbito do Programa de P&D da ANEEL (PD-07267-0012/2018).”

“This research is part of the project entitled 'Portfolio Analysis of Generation Plants to Meet Future Load of the National Interconnected System - Robust Energy Matrix', financed by EDP under the ANEEL R&D Program (PD-07267-0012/2018).”

## Time de desenvolvimento

O time de desenvolvimento é formado por membros da equipe Venidera:

* [André Toscano](https://github.com/aemitos)
* [João Borsói Soares](https://github.com/joaoborsoi)
* [Renan de Paula Maciel]()

## Licença

http://www.apache.org/licenses/LICENSE-2.0
