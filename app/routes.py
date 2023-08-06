from app import app
from flask import render_template, url_for, g, redirect, request
from flask_babel import gettext, _, get_locale

import json
import bibtexparser

@app.before_request
def before_request():
    g.locale = str(get_locale())


def get_catalog():
    if 'catalog' not in g:
        with open(app.config['CSMELL_CATALOG_JSON']) as file:
            g.catalog = json.load(file)
    return g.catalog


def get_library():
    if 'library' not in g:
        references = ''
        with open(app.config['BIBTEX_REFERENCES'], "r", encoding='utf8') as arquivo:
            for i in arquivo.readlines():
                references += i

        g.library = bibtexparser.bparser.parse(references)
        g.library_ids = {}
        for index, entry in enumerate(g.library.entries):
            g.library_ids[entry['ID']] = index

    return g.library


def clean_factors(factors):
    codes = set()
    for c in factors:
        codes.add(c[1])

    codes = str(codes)
    codes = codes.replace('{', '')
    codes = codes.replace('}', '')
    codes = codes.replace('\'', '')
    return codes


@app.route('/')
@app.route('/index')
def index():
    smells = get_catalog()

    page = request.args.get('page', 1, type=int)
    per_page = app.config['SMELL_PER_PAGE']
    max_page = int(app.config['TOTAL_SMELL']/app.config['SMELL_PER_PAGE'])

    keys = list(smells.keys())
    total = page * per_page
    start = (page-1) * per_page

    prev_page = max(1, page-1)
    next_page = page+1

    page_keys = keys[start:total]
    page_smells = {}
    for k in page_keys:
        page_smells[k] = smells[k]

    return render_template('index.html', title='Home', smells=page_smells,
                            prev_page=prev_page, next_page=next_page, max_page=max_page)


@app.route('/tools')
def tools():
    return render_template('tools.html', title='Tools')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/references')
def references():
    bibtex = get_library()

    return render_template('references.html', references=bibtex.entries)


@app.route('/community-smells')
def community_smells():
    smells = get_catalog()

    page = request.args.get('page', 1, type=int)
    per_page = app.config['SMELL_PER_PAGE']
    max_page = int(app.config['TOTAL_SMELL']/app.config['SMELL_PER_PAGE'])

    keys = list(smells.keys())
    total = page * per_page
    start = (page-1) * per_page

    prev_page = max(1, page-1)
    next_page = page+1

    page_keys = keys[start:total]
    page_smells = {}
    for k in page_keys:
        page_smells[k] = smells[k]

    return render_template('home.html', title='Community Smells', smells=page_smells,
                            prev_page=prev_page, next_page=next_page, max_page=max_page)


@app.route('/smell/<tagname>')
def smell(tagname=None):
    catalog = get_catalog()
    if tagname is None or tagname not in catalog.keys():
        redirect(url_for('index'))

    keys = list(catalog.keys())
    smell = catalog[tagname]

    cause_codes = clean_factors(smell['causes'])
    effect_codes = clean_factors(smell['effects'])


    refs = []
    for i in smell['refactoring']:
        refs.append(i['ref'])


    refs.extend(smell['refs'])

    print(refs)
    references = []
    bibtex = get_library()
    for bib in bibtex.entries:
        if bib['ID'] in refs:
            print(bib['ID'])
            references.append(bib)


    id = int(smell['id'])

    prev_smell = smell['tagname']
    if id>1:
        prev_smell = keys[ id-2 ]

    next_smell = smell['tagname']
    if id<30:
        next_smell = keys[ id ]

    return render_template('smell.html', title=smell['title'], smell=smell, cause_codes=cause_codes,
                           effect_codes=effect_codes, references=references, prev_smell=prev_smell, next_smell=next_smell)


