from setuptools import setup, find_packages
__version__ = '1.0.1'

long_desc = """Deckparser

O Deckparser é um pacote Python que implementa importadores de dados para os arquivos de entrada dos modelos oficiais do sistema elétrico brasileiro.
Os modelos NEWAVE, DECOMP e DESSEM são os formatos contemplados. Estes modelos são produzidos pelo CEPEL Eletrobrás.
O arquivo de dados é denominado deck, talvez por herança do nome utilizado para conjunto de cartões de entrada de dados de sistemas computacionais dos anos 70.
Um deck consiste de um arquivo, geralmente zipado, que mantém arquivos de dados em formato binário e texto simples.
Os formatos são definidos e estruturados considerando conceitos do Fortran para a definição de dados de entrada. Assim, para os arquivos de dados baseados em texto pode ser realizado o parsing simples para aquisição dos dados.
Para os arquivos binários é utilizado o pacote Python Numpy, que suporta a abertura e leitura de arquivos de dados binários do Fortran.
"""

if __name__ == '__main__':
    project_name = "deckparser"
    setup(
        name=project_name,
        version=__version__,
        author="Andre E Toscano",
        author_email="andre@venidera.com",
        description=("NEWAVE, DECOMP and DESSEM deck parser."),
        license="Apache 2.0",
        keywords="parser deck newave",
        url="https://github.org/venidera/deckparser",
        packages=find_packages(),
        install_requires=['numpy', 'unidecode'],
        long_description=long_desc,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Operating System :: Unix",
            "Topic :: Utilities",
        ],
        test_suite=project_name + '.tests',
        scripts=['bin/decomp2json', 'bin/dessem2json'],
        package_data={'deckparser.importers.dessem.cfg': ['*.xml'],
                      'deckparser.importers.dessem.out.cfg': ['*.json']},
        include_package_data=True
    )
