#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A service that provides JSON and RESTful lookups to webdict xml trie files.

## Configuration

Configuration settings for paths to FSTs, utility programs and
dictionary files must be set in `app.config.yaml`. A sample file is
checked in as `app.config.yaml.in`, so copy this file, edit the settings
and then launch the service.

## Testing via cURL

### Submit post data with JSON

    curl -X POST -H "Content-type: application/json" \
         -d ' {"lookup": "fest" } ' \
         http://localhost:5000/lookup/nob/sme/

### Submit GET data with parameters, and JSON response

    curl -X GET -H "Content-type: application/json" \
           http://localhost:5000/detail/sme/nob/geađgi/

## Installing

See requirements.txt. Ideally, use virtualenv to create a new Python
virtual environment, and use requirements.txt to automatically install
all of the required packages.

You can test that it's worked by running this file with python-- if you
see no errors, and dictionaries are parsed, and autocomplete tries are
prepared, things are working. Finally, the app will state which host and
port it is running on. For developing locally, this is all you need.

### Production environments

There is a separate fcgi script (neahttadigisanit.fcgi) which is meant
to be used with nginx for production environments.

## Todos

TODO: autocomplete from all left language lemmas, build cache and save
      to pickle on each run, then use pickle

## Compiling XML

    java -Xmx2048m -Dfile.encoding=UTF8 net.sf.saxon.Transform \
        -it:main /path/to/gtsvn/words/scripts/collect-dict-parts.xsl \
        inDir=/path/to/gtsvn/words/dicts/smenob/src/ > OUTFILE.xml

    may need to also include -cp ~/lib/saxon9.jar

### Note about macs with saxon

Can be installed by brew

    brew install saxon

"""

import sys
import logging
import urllib
from   flask                          import ( Flask
                                             , request
                                             , redirect
                                             , session
                                             , json
                                             , render_template
                                             , Markup
                                             , Response
                                             , abort
                                             )

from   werkzeug.contrib.cache         import SimpleCache
from   config                         import Config
from   utils                          import *
from   logging                        import getLogger

from   flaskext.babel                 import Babel
from   flaskext.babel                 import gettext as _


cache = SimpleCache()
app = Flask(__name__,
    static_url_path='/static',)

app.jinja_env.line_statement_prefix = '#'
app.jinja_env.add_extension('jinja2.ext.i18n')
app.config['cache'] = cache
app.config = Config('.', defaults=app.config)
app.config.from_yamlfile('app.config.yaml')

from morpho_lexicon import MorphoLexicon
app.morpholexicon = MorphoLexicon(app.config)

try:
    with open('secret_key.do.not.check.in', 'r') as F:
        key = F.readlines()[0].strip()
    app.config['SECRET_KEY'] = key
except IOError:
    print >> sys.stderr, """
    You need to generate a secret key, and store it in a file with the
    following name: secret_key.do.not.check.in """
    sys.exit()

babel = Babel(app)
babel.init_app(app)

# Configure user_log
user_log = getLogger("user_log")
useLogFile = logging.FileHandler('user_log.txt')
user_log.addHandler(useLogFile)
user_log.setLevel("INFO")

AVAILABLE_LOCALES = [ 'se'
                    , 'no'
                    , 'fi'
                    ]

AVAILABLE_LOCALE_ISO_TRANSFORM = {
    'se': 'sme',
    'no': 'nob',
    'fi': 'fin',
    'en': 'eng',
    'sma': 'sma',
}

## These things are sort of a temporary fix for some of the localization
## that runs off of CSS selectors, in order to include the 3 digit ISO
## into the <body /> @lang attribute.

def iso_filter(_iso):
    return AVAILABLE_LOCALE_ISO_TRANSFORM.get(_iso, _iso)

@app.before_request
def append_session_globals():
    loc = get_locale()
    app.jinja_env.globals['session_locale'] = loc
    app.jinja_env.globals['session_locale_long_iso'] = iso_filter(loc)

@babel.localeselector
def get_locale():
    ses_lang = session.get('locale', None)
    if ses_lang is not None:
        return ses_lang
    else:
        ses_lang = 'se'
        if 'baakoeh' in request.host:
            ses_lang = 'no'
        elif (u'sanit' in request.host) or (u'sánit' in request.host):
            ses_lang = 'se'
        else:
            ses_lang = request.accept_languages.best_match(AVAILABLE_LOCALES)
        session.locale = ses_lang
        app.jinja_env.globals['session'] = session
    return ses_lang

##
##  Endpoints
##
##


# language_pairs = app.config.lexicon.language_pairs
# autocomplete_tries = app.config.lexicon.autocomplete_tries

##
## Template filters
##

@app.template_filter('iso_to_i18n')
def append_language_names_i18n(s):
    from language_names import NAMES
    return NAMES.get(s, s)

@app.template_filter('to_xml_string')
def to_xml_string(n):
    from lxml import etree
    return etree.tostring(n, pretty_print=True, encoding="utf-8").decode('utf-8')


@app.template_filter('tagfilter')
def tagfilter(s, lang_iso):
    if not s:
        return s
    filters = app.config.tag_filters.get(lang_iso, False)
    if filters:
        filtered = []
        if isinstance(s, list):
            parts = s
        else:
            parts = s.split(' ')
        for part in parts:
            filtered.append(filters.get(part.lower(), part))
        return ' '.join([a for a in filtered if a.strip()])
    else:
        if isinstance(s, list):
            return ' '.join(s)
        else:
            return s


@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/autocomplete/<from_language>/<to_language>/',
           methods=['GET'], endpoint="autocomplete")
def autocomplete(from_language, to_language):

    autocomplete_tries = app.config.lexicon.autocomplete_tries
    # URL parameters
    lookup_key   = request.args.get('lookup', False)
    lemmatize    = request.args.get('lemmatize', False)
    has_callback = request.args.get('callback', False)

    autocompleter = autocomplete_tries.get((from_language, to_language), False)

    if not autocompleter:
        return fmtForCallback(
                json.dumps(" * No autocomplete for this language pair."),
                has_callback)

    autos = autocompleter.autocomplete(lookup_key)

    # Only lemmatize if nothing returned from autocompleter?

    return Response(response=fmtForCallback(json.dumps(autos), has_callback),
                    status=200,
                    mimetype="application/json")

@app.route('/lookup/<from_language>/<to_language>/',
           methods=['GET'], endpoint="lookup")
def lookupWord(from_language, to_language):
    """
    Returns a simplified set of JSON for dictionary, with 'success' to mark
    whether there were no errors. Additional URL parameters are available to
    control the lookup type or whether the lookup is lemmatized before being
    run through the lexicon.

    Path parameters:

        /lookup/<from_language>/<to_language>/

        Follow the ISO code.

        TODO: 404 error for missing languages

    URL parameters:

        lookup - the string to search for
        lemmatize - true/false
        type - none, or 'startswith'

    Output:

        {
            "result": [
                {
                    "input": "viidni",
                    "lookups": [
                        {
                            "right": [
                                "vin"
                            ],
                            "pos": "n",
                            "left": "viidni"
                        }
                    ]
                }
            ],
            "success": true
        }

    If there are multiple results from lemmatizing, they are included in the
    "results" list.

    """
    from lexicon import SimpleJSON

    if (from_language, to_language) not in app.config.dictionaries:
        abort(404)

    success = False

    # URL parameters
    lookup_key = user_input = request.args.get('lookup', False)
    # TODO: remove option from JS
    lemmatize               = request.args.get('lemmatize', False)
    has_callback            = request.args.get('callback', False)
    pretty                  = request.args.get('pretty', False)

    if lookup_key is False:
        return json.dumps(" * lookup undefined")

    def filterPOS(r):
        def fixTag(t):
            t_pos = t.get('pos', False)
            if not t_pos:
                return t
            t['pos'] = tagfilter(t_pos, from_language)
            return t
        return fixTag(r)

    mlex = app.morpholexicon

    xml_nodes, analyses = mlex.lookup( lookup_key
                                     , source_lang=from_language
                                     , target_lang=to_language
                                     , split_compounds=True
                                     , non_compound_only=True
                                     , no_derivations=True
                                     )

    if analyses:
        def filterPOSAndTag(analysis):
            filtered_pos = tagfilter(analysis.pos, from_language)
            joined = filtered_pos + ' ' + ' '.join(analysis.tag)
            return (analysis.lemma, joined)
        tags = map(filterPOSAndTag, analyses)
    else:
        tags = []

    result = SimpleJSON( xml_nodes
                       , target_lang=to_language
                       )

    result = map(filterPOS, list(result))

    if len(result) > 0:
        success = True

    result_with_input = [{'input': lookup_key, 'lookups': result}]

    logSimpleLookups( user_input
                    , result_with_input
                    , from_language
                    , to_language
                    )

    data = json.dumps({ 'result': result_with_input
                      , 'tags': tags
                      , 'tag_msg': _(" is a possible form of ... ")
                      , 'success': success
                      })

    if pretty:
        data = json.dumps( json.loads(data)
                         , sort_keys=True
                         , indent=4
                         , separators=(',', ': ')
                         )

    if has_callback:
        data = '%s(%s)' % (has_callback, data)

    return Response( response=data
                   , status=200
                   , mimetype="application/json"
                   )


# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
@app.route('/detail/<from_language>/<to_language>/<wordform>.<format>',
           methods=['GET'], endpoint="detail")
def wordDetail(from_language, to_language, wordform, format):
    """
    Returns a detailed set of information, in JSON or HTML, given a specific
    wordform.

    Path parameters:

        /detail/<from_language>/<to_language>/<wordform>.<format>

    TODO: See /languages for an overview of supported language pairs, and
    supply the ISO code for <from_language> and <to_language>. <wordform> may
    be any word form in the source language, as the form will be passed through
    a morphological analyzer.

    <format> must be either json, or html.

      Ex.) /detail/sme/nob/orrut.html
           /detail/sme/nob/orrut.json

    <wordform> is generally expected to be UTF-8, and most web browsers
    automatically encode unicode in URLs to UTF-8, however it may be that
    services using this endpoint will need to make sure to do the conversion.

    """
    from lexicon import DetailedFormat

    user_input = wordform
    if not format in ['json', 'html']:
        return _("Invalid format. Only json and html allowed.")

    wordform = decodeOrFail(wordform)

    # NOTE: these options are mostly for detail views that are linked to
    # from the initial page's search. Everything should work without
    # them, and with all or some of them.

    # Do we filter analyzed forms and lookups by pos?
    pos_filter = request.args.get('pos_filter', False)
    # Should we match the input lemma with the analyzed lemma?
    lemma_match = request.args.get('lemma_match', False)
    # From the front page-- match the hash of the lxml element
    e_node = request.args.get('e_node', False)

    # Do we want to analyze compounds?
    no_compounds = request.args.get('no_compounds', False)

    # Cache key by URL
    entry_cache_key = u'%s?%s' % (request.path, request.query_string)

    if no_compounds or lemma_match:
        want_more_detail = True
    else:
        want_more_detail = False

    def unsupportedLang(more='.'):
        if format == 'json':
            _err = " * Detailed view not supported for this language pair"
            return json.dumps(_err + " " + more)
        elif format == 'html':
            abort(404)

    if app.caching_enabled:
        cached_result = cache.get(entry_cache_key)
    else:
        cached_result = None

    if cached_result is None:

        lang_paradigms = app.config.paradigms.get(from_language)
        if not lang_paradigms:
            unsupportedLang(', no paradigm defined.')

        morph = app.config.morphologies.get(from_language, False)

        if no_compounds:
            _split = True
            _non_c = True
            _non_d = False
        else:
            _split = True
            _non_c = False
            _non_d = False

        mlex = app.morpholexicon
        xml_nodes, analyses = mlex.lookup( wordform
                                         , source_lang=from_language
                                         , target_lang=to_language
                                         , split_compounds=_split
                                         , non_compounds_only=_non_c
                                         , no_derivations=_non_d
                                         )

        # TODO: move generation to detailed format? thus node correct
        # pos, tags, etc., are available
        res = list(DetailedFormat(xml_nodes, target_lang=to_language))

        lex_results = []
        for r in res:
            lemma = r.get('lemma')
            pos = r.get('pos')
            _type = r.get('type')
            input_info = (lemma, pos, '', _type)
            lex_results.append({
                'entries': r,
                'input': input_info,
            })

        def _byPOS(r):
            if r.get('input')[1].upper() == pos_filter.upper():
                return True
            else:
                return False

        def _byLemma(r):
            if r.get('input')[0] == wordform:
                return True
            else:
                return False

        def _byNodeHash(r):
            node = r.get('entries').get('entry_hash')
            if node == e_node:
                return True
            else:
                return False

        if e_node:
            lex_results = filter(_byNodeHash, lex_results)
        if pos_filter:
            lex_results = filter(_byPOS, lex_results)
        if lemma_match:
            lex_results = filter(_byLemma, lex_results)

        analyses = [(l.lemma, l.pos, l.tag) for l in analyses]

        try:
            node_texts = [ to_xml_string(n.get('entries').get('node'))
                           for n in lex_results
                           if n.get('entries').get('node') ]
        except:
            node_texts = []

        detailed_result = {
            "input": wordform,
            "analyses": analyses,
            "lexicon": lex_results,
            "node_texts": node_texts
        }

        # Generate each paradigm.
        for _r in lex_results:
            lemma, pos, tag, _type = _r.get('input')
            try:
                node = _r.get('entries').get('node')
            except:
                node = False

            paradigm = lang_paradigms.get(pos.upper())

            if paradigm:
                _pos_type = [pos]
                if _type:
                    _pos_type.append(_type)
                form_tags = [_pos_type + _t.split('+') for _t in paradigm]

                _generate = morph.generate(lemma, form_tags, node)
                _r['paradigms'] = _generate
            else:
                _r['paradigms'] = False

        cache.set(entry_cache_key, detailed_result)
    else:
        detailed_result = cached_result

    _lookup = detailed_result.get('lexicon')

    if len(_lookup) > 0:
        success = True
        result_lemmas = list(set([
            entry['input'][0] for entry in detailed_result['lexicon']
        ]))
        _meanings = []
        for lexeme in detailed_result['lexicon']:
            if lexeme['entries']:
                _entry_tx = []
                for mg in lexeme['entries']['meaningGroups']:
                    _entry_tx.append(mg['translations'])
                _meanings.append(_entry_tx)
        tx_set = '; '.join([', '.join(a) for a in _meanings])
    else:
        success = False
        result_lemmas = ['-']
        tx_set = '-'

    user_log.info('%s\t%s\t%s\t%s\t%s\t%s' % ( user_input
                                             , str(success)
                                             , ', '.join(result_lemmas)
                                             , tx_set
                                             , from_language
                                             , to_language
                                             )
                 )

    if format == 'json':
        result = json.dumps({
            "success": True,
            "result": detailed_result
        })
        return result
    elif format == 'html':
        return render_template( 'word_detail.html'
                              , language_pairs=app.config.pair_definitions
                              , result=detailed_result
                              , user_input=user_input
                              , _from=from_language
                              , _to=to_language
                              , more_detail_link=want_more_detail
                              , zip=zipNoTruncate
                              )


@app.route('/read/', methods=['GET'])
def bookmarklet():
    from bookmarklet_code import bookmarklet_escaped
    bkmklt = bookmarklet_escaped
    return render_template('reader.html', bookmarklet=bkmklt)

##
## Public Docs
##

# @app.route('/lookup/', methods=['GET'], endpoint="lookup-doc")
# def wordLookupDocs():
#     from cgi import escape
#     _lookup_doc = escape(lookupWord.__doc__)
#     return '<html><body><pre>%s</pre></body></html>' % _lookup_doc

# @app.route('/detail/', methods=['GET'], endpoint="detail-doc")
# def wordDetailDocs():
#     from cgi import escape
#     _lookup_doc = escape(wordDetail.__doc__)
#     return '<html><body><pre>%s</pre></body></html>' % _lookup_doc

##
## Public pages
##

# For direct links, form submission.
@app.route('/<_from>/<_to>/', methods=['GET', 'POST'])
def indexWithLangs(_from, _to):
    from lexicon import FrontPageFormat

    mlex = app.morpholexicon

    user_input = lookup_val = request.form.get('lookup', False)

    if (_from, _to) not in app.config.dictionaries:
        abort(404)

    successful_entry_exists = False
    errors = []

    results = False
    analyses = False

    if request.method == 'POST' and lookup_val:

        mlex = app.morpholexicon

        xml_nodes, analyses = mlex.lookup( lookup_val
                                         , source_lang=_from
                                         , target_lang=_to
                                         , split_compounds=True
                                         )

        analyses = [(lem.input, lem.lemma, [lem.pos] + lem.tag)
                    for lem in analyses]

        fmtkwargs = {'target_lang': _to}
        # [(lemma, XMLNodes)] -> [(lemma, generator(AlmostJSON))]
        formatted_results = list(FrontPageFormat(xml_nodes, **fmtkwargs))

        # When to display unknowns
        successful_entry_exists = False
        if len(formatted_results) > 0:
            successful_entry_exists = True

        results = sorted( formatted_results
                        , key=lambda (r): len(r.get('left'))
                        , reverse=True
                        )

        results = [ {'input': lookup_val, 'lookups': results} ]

        logIndexLookups(user_input, results, _from, _to)

        show_info = False
    else:
        user_input = ''
        show_info = True

    if len(errors) == 0:
        errors = False

    # TODO: include form analysis of user input #formanalysis
    return render_template( 'index.html'
                          , language_pairs=app.config.pair_definitions
                          , _from=_from
                          , _to=_to
                          , user_input=lookup_val
                          , word_searches=results
                          , analyses=analyses
                          , errors=errors
                          , show_info=show_info
                          , zip=zipNoTruncate
                          , successful_entry_exists=successful_entry_exists
                          )

@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/plugins/', methods=['GET'])
def plugins():
    return render_template('plugins.html')

@app.route('/locale/<iso>/', methods=['GET'])
def set_locale(iso):
    from flaskext.babel import refresh

    session['locale'] = iso
    # Refresh the localization infos, and send the user back whence they
    # came.
    refresh()
    ref = request.referrer
    if ref is not None:
        return redirect(request.referrer)
    else:
        return redirect('/')

@app.route('/', methods=['GET'], endpoint="canonical-root")
def index():
    return render_template( 'index.html'
                          , language_pairs=app.config.pair_definitions
                          , internationalizations=AVAILABLE_LOCALES
                          , _from='sme'
                          , _to='nob'
                          , show_info=True
                          )


if __name__ == "__main__":
    app.caching_enabled = True
    app.run(debug=True, use_reloader=False)

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :
