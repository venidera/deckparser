DeckParser: Um leitor de dados do NEWAVE, DECOMP and DESSEM
=============================================

![GitHub Release](https://img.shields.io/badge/release-v0.0.1-blue.svg)
![GitHub license](https://img.shields.io/badge/license-Apachev2-yellow.svg)

DeckParser fornece programas para abrir e ler os dados dos programas NEWAVE, DECOMP e DESSEM

* Projeto em desenvolvimento - não aberto ainda para contribuições da comunidade (pull requests)

## Dependências

* Python > 3.6.x

## Leitura de arquivos validada:

* SISTEMA.DAT: ok

## Uso

* Exemplo 1: ler arquivo `SISTEMA.DAT`:

```python
from deckparser.deckzipped import DeckZipped
from deckparser.importers.importDGER import importDGER
from deckparser.importers.importSISTEMA import importSISTEMA

dz = DeckZipped('/Users/andre/git/deckparser/test/NW201305.zip')
dger = importDGER(dz.openFile(fnp='dger'))
SISTEMA = importSISTEMA(dz.openFileExtData(fnp='sistema'),dger)
```

* Example 2: ler deck dentro de um `dict`:

```python
from deckparser.deck2dicts import deck2dicts
deck = deck2dicts('/Users/andre/git/deckparser/test/NW201305.zip')
```

## Instalação

Usando pip:

```bash
pip install git+ssh://git@github.com:venidera/deckparser.git
```

## Time de desenvolvimento

* [André Toscano](https://github.com/aemitos)
* [João Borsói Soares](https://github.com/joaoborsoi)
* [Renan]()

## Licença

http://www.apache.org/licenses/LICENSE-2.0

