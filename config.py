import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e5d09a98fb37bca08f46abfeb695ddebd35a4627eb8b5325f18b0c17292a765c'
    LANGUAGES = ['en', 'es', 'pt-BR']
    SMELL_PER_PAGE = 5
    TOTAL_SMELL = 30
    CSMELL_CATALOG_JSON = 'csmell-catalog.json'
    BIBTEX_REFERENCES = 'references.bib'
