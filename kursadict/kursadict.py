#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A service that provides JSON and RESTful lookups to webdict xml trie files.

## Configuration

Configuration settings for paths to FSTs, utility programs and
dictionary files must be set in `app.config.yaml`. A sample file is
checked in as `app.config.yaml.in`, so copy this file, edit the settings
and then launch the service.

## Endpoints

### /lookup/<from_language>/<to_language>/

See below in function docstring


### /auto/<language>

Autocomplete for jQuery's autocomplete plugin, available from:
  http://jqueryui.com/autocomplete/

TODO: return array of lemmas formatted such:

    [ { label: "Choice1", value: "value1" }, ... ]

## Testing via cURL

### Submit post data with JSON

    curl -X POST -H "Content-type: application/json" \
         -d ' {"lookup": "fest" } ' \
         http://localhost:5000/lookup/nob/sme/

### Submit GET data with parameters, and JSON response

    curl -X GET -H "Content-type: application/json" \
           http://localhost:5000/detail/sme/nob/geađgi/

## Installing

TODO: document flask installation

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

from lxml import etree
from flask import Flask, request, json, render_template, Markup
from werkzeug.contrib.cache import SimpleCache
from crossdomain import crossdomain
from config import settings

cache = SimpleCache()
app = Flask(__name__,
    static_url_path='/kursadict/static',)

useLogFile = logging.FileHandler('user_log.txt')
app.logger.addHandler(useLogFile)


##
##  Lexicon
##
##

class XMLDict(object):
    """ XML dictionary class. Initiate with a file path or an already parsed
    tree, exposes methods for searching in XML.

    Entries are only cleaned resulting in lg/l/text(), lg/l@pos, and
    mg/tg/t/text() with self.cleanEntry. Probably easier to make mixins
    that add to this functionality?
    """
    def __init__(self, filename=False, tree=False):
        if not tree:
            print "parsing %s" % filename
            self.tree = etree.parse(filename)
        else:
            self.tree = tree
        self.xpath_evaluator = etree.XPathDocumentEvaluator(self.tree)

        # Initialize XPath queries
        regexpNS = "http://exslt.org/regular-expressions"
        self.lemmaStartsWith = etree.XPath('.//e[starts-with(lg/l/text(), $lemma)]')
        self.lemma = etree.XPath('.//e[lg/l/text() = $lemma]')
        self.lemmaPOS = etree.XPath(".//e[lg/l/text() = $lemma and re:match(lg/l/@pos, $pos, 'i')]",
                                    namespaces={'re':regexpNS})
        self.lemmaPOSAndType = etree.XPath(".//e[lg/l/text() = $lemma and re:match(lg/l/@pos, $pos, 'i') and lg/l/@type = $_type]",
                                    namespaces={'re':regexpNS})

    def cleanEntry(self, e):
        l = e.find('lg/l')
        left_text = l.text
        left_pos = l.get('pos')
        ts = e.findall('mg/tg/t')
        right_text = [t.text for t in ts]
        return {'left': left_text, 'pos': left_pos, 'right': right_text}

    def XPath(self, xpathobj, *args, **kwargs):
        print "Querying: %s" % xpathobj.path
        print "With: %s, %s" % (repr(args), repr(kwargs))
        return map(self.cleanEntry, xpathobj(self.tree, *args, **kwargs))

    def lookupLemmaStartsWith(self, lemma):
        return self.XPath(self.lemmaStartsWith, lemma=lemma)

    def lookupLemma(self, lemma):
        return self.XPath(self.lemma, lemma=lemma)

    def lookupLemmaPOS(self, lemma, pos):
        return self.XPath(self.lemmaPOS, lemma=lemma, pos=pos)

    def lookupLemmaPOSAndType(self, lemma, pos, _type):
        return self.XPath(self.lemmaPOSAndType, lemma=lemma, pos=pos, _type=_type)

class DetailedEntries(XMLDict):
    def cleanEntry(self, e):
        l = e.find('lg/l')
        mg = e.findall('mg')

        meaningGroups = []
        for tg in e.findall('mg/tg'):
            _ex = [(xg.find('x').text, xg.find('xt').text) for xg in tg.findall('xg')]
            _tg = {
                'translations': [t.text for t in tg.findall('t')],
                'examples': _ex
            }
            meaningGroups.append(_tg)

        return {
            'lemma': l.text,
            'pos': l.get('pos'),
            'context': l.get('context'),
            'meaningGroups': meaningGroups,
            'type': l.get('type')
        }

class ReverseLookups(XMLDict):
    """

    1. use only entries that have the attribute usage="vd" at entry
    level

    2. don't use entries with reverse="no" at entry level

    3. search by e/mg/tg/t/text() instead of /e/lg/l/text()

    """

    def cleanEntry(self, e):
        ts = e.findall('mg/tg/t')
        ts_text = [t.text for t in ts]
        ts_pos = [t.get('pos') for t in ts]

        l = e.find('lg/l')
        right_text = [l.text]

        return {'left': ts_text, 'pos': ts_pos, 'right': right_text}

    def lookupLemmaStartsWith(self, lemma):
        _xpath = './/e[mg/tg/t/starts-with(text(), "%s")]' % lemma
        return self.XPath(_xpath)

    def lookupLemma(self, lemma):
        _xpath = './/e[mg/tg/t/text() = "%s" and @usage = "vd" and not(@reverse)]'
        return self.XPath(_xpath % lemma)

    def lookupLemmaPOS(self, lemma, pos):
        _xpath = ' and '.join(
            [ './/e[mg/tg/t/text() = "%s"' % lemma
            , '@usage = "vd"'
            , 'not(@reverse)'
            , 'mg/tg/t/@pos = "%s"]' % pos.lower()
            ]
        )
        return self.XPath(_xpath)


language_pairs = dict(
    [ (k, XMLDict(filename=v))
      for k, v in settings.dictionaries.iteritems() ]
)

# reverse_language_pairs = dict(
#     [ ((k[1], k[0]), ReverseLookups(filename=v))
#       for k, v in settings.reversable_dictionaries.iteritems() ]
# )

reverse_language_pairs = {}

for k, v in settings.reversable_dictionaries.iteritems():
    has_root = language_pairs.get((k[0], k[1]))
    if has_root:
        reverse_language_pairs[(k[1], k[0])] = ReverseLookups(tree=has_root.tree)
    else:
        reverse_language_pairs[(k[1], k[0])] = ReverseLookups(filename=v)

language_pairs.update(reverse_language_pairs)

def lookupXML(_from, _to, lookup, lookup_type=False):
    _dict = language_pairs.get((_from, _to), False)
    if _dict:
        if lookup_type:
            if lookup_type == 'startswith':
                return {'lookups': _dict.lookupLemmaStartsWith(lookup)}
        return {'lookups': _dict.lookupLemma(lookup)}

    else:
        return {'error': "Unknown language pair"}


def detailedLookupXML(_from, _to, lookup, pos, _type=False):
    lexicon = language_pairs.get((_from, _to), False)
    # wrap in mixin for detailed results
    detailed_tree = DetailedEntries(tree=lexicon.tree)

    if lexicon and detailed_tree:
        # TODO: include PoS
        if _type:
            if _type.strip():
                return {'lookups': detailed_tree.lookupLemmaPOSAndType(lookup, pos, _type)}
        return {'lookups': detailed_tree.lookupLemmaPOS(lookup, pos)}
    else:
        return {'error': "Unknown language pair"}

##
##  Lemmatization
##
##


def encodeOrFail(S):
    try:
        return S.encode('utf-8')
    except:
        return S

def decodeOrFail(S):
    try:
        return S.decode('utf-8')
    except:
        return S


morphologies = settings.morphologies

##
##  Endpoints
##
##

@app.route('/kursadict/lookup/<from_language>/<to_language>/',
           methods=['GET'])
@crossdomain(origin='*')
def lookupWord(from_language, to_language):
    """
    Returns a simplified set of JSON for dictionary, with 'success' to mark
    whether there were no errors. Additional URL parameters are available to
    control the lookup type or whether the lookup is lemmatized before being
    run through the lexicon.

    Path parameters:

        /kursadict/lookup/<from_language>/<to_language>/

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

    success = False
    results = False

    # URL parameters
    lookup_key = user_input = request.args.get('lookup', False)
    lookup_type = request.args.get('type', False)
    lemmatize = request.args.get('lemmatize', False)

    if lemmatize and not lookup_type:
        lemm_ = morphologies.get(from_language, False)
        if lemm_:
            lemmatizer = lemm_.lemmatize
        lemmatized_lookup_key = lemmatizer(lookup_key, split_compounds=True)
    else:
        lemmatized_lookup_key = False

    if lemmatized_lookup_key:
        if not isinstance(lemmatized_lookup_key, list):
            lemmatized_lookup_key = [lemmatized_lookup_key]

        results = []
        for _key in lemmatized_lookup_key:
            result = lookupXML(from_language, to_language,
                               _key, lookup_type)
            result['input'] = _key
            if len(result['lookups']) == 0:
                result['lookups'] = False
            results.append(result)

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)

        if 'error' in result:
            success = False
        else:
            success = True

        if 'lookups' in result:
            if not result['lookups']:
                success = False
    else:

        result = lookupXML(from_language, to_language,
                           lookup_key, lookup_type)
        result['input'] = lookup_key
        if len(result['lookups']) == 0:
            result['lookups'] = False
        results = [result]

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)

        if 'error' in result:
            success = False
        else:
            success = True

        if 'lookups' in result:
            if not result['lookups']:
                success = False

    result_lemmas = set()
    tx_set = set()
    if success:
        for result in results:
            result_lookups = result.get('lookups')
            if result_lookups:
                for lookup in result_lookups:
                    l_left = lookup.get('left')
                    l_right = ', '.join(lookup.get('right'))
                    tx_set.add(l_right)
                    # Reversed lookups return list
                    if isinstance(l_left, list):
                        for _l in l_left:
                            result_lemmas.add(_l)
                    else:
                        result_lemmas.add(lookup.get('left'))

    result_lemmas = ', '.join(list(result_lemmas))
    meanings = '; '.join(list(tx_set))

    app.logger.info('%s\t%s\t%s\t%s' % (user_input, str(success), result_lemmas, meanings))

    return json.dumps({
        'result': results,
        'success': success
    })


@app.route('/kursadict/detail/<from_language>/<to_language>/<wordform>.<format>',
           methods=['GET'])
@crossdomain(origin='*')
def wordDetail(from_language, to_language, wordform, format):
    """
    Returns a detailed set of information, in JSON or HTML, given a specific
    wordform.

    Path parameters:

        /kursadict/detail/<from_language>/<to_language>/<wordform>.<format>
    
    See /kursadict/languages for an overview of supported language pairs, and
    supply the ISO code for <from_language> and <to_language>. <wordform> may
    be any word form in the source language, as the form will be passed through
    a morphological analyzer.

    <format> must be either json, or html.
    
      Ex.) /kursadict/detail/sme/nob/orrut.html
           /kursadict/detail/sme/nob/orrut.json

    <wordform> is generally expected to be UTF-8, and most web browsers
    automatically encode unicode in URLs to UTF-8, however it may be that
    services using this endpoint will need to make sure to do the conversion.

    """
    import hashlib

    user_input = wordform
    if not format in ['json', 'html']:
        return "Invalid format. Only json and html allowed."

    cache_key = '/detail/%s/%s/%s.%s' % (from_language, to_language, wordform, format)
    wordform = wordform.encode('utf-8')

    if (from_language, to_language) in reverse_language_pairs:
        if format == 'json':
            return json.dumps(" * Detailed view not supported for this language pair")
        elif format == 'html':
            return " * Detailed view not supported for this language pair"

    if app.caching_enabled:
        cached_result = cache.get(cache_key)
    else:
        cached_result = None

    if cached_result is None:

        lang_paradigms = settings.paradigms.get(from_language)
        lang_baseforms = settings.baseforms.get(from_language)
        # All lookups in XML must go through analyzer, because we need POS
        # info for a good lookup.
        morph = morphologies.get(from_language, False)
        analyzed = morph.analyze(wordform, split_compounds=True)

        def lemmaLen(a):
            return len(a[1])

        # Collect lemmas and tags
        _result_formOf = []
        if analyzed:
            for form, lemma, tag in sorted(analyzed, key=lemmaLen, reverse=True):

                # TODO: try with OBT
                if lemma == '?' or tag == '?':
                    continue
                pos, _tag = tag[0], tag[1::]
                _ft = morph.tool.formatTag(tag)
                _result_formOf.append((lemma, pos, _ft))

        # Now collect XML lookups
        _result_lookups = []
        _lemma_pos_exists = []

        for lemma, pos, tag in _result_formOf:

            # TODO: generalize for other languages
            _sp = morph.tool.splitAnalysis(tag)
            if len(_sp) >= 2:
                _type = _sp[1]
                if _type not in [u'NomAg', 'G3']:
                    _type = False
            else:
                _type = False

            if (lemma, pos) in _lemma_pos_exists:
                continue
            # Only look up word when there is a baseform
            paradigm = lang_paradigms.get(pos)
            baseforms = lang_baseforms.get(pos, False)
            if baseforms:
                xml_result = detailedLookupXML(from_language,
                                               to_language,
                                               lemma,
                                               pos,
                                               _type=_type)

                if len(xml_result['lookups']) == 0:
                    xml_result = False

                _result_lookups.append({
                    'entries': xml_result,
                    'input': (lemma, pos, tag, _type)
                })
                _lemma_pos_exists.append((lemma, pos))
            else:
                continue

        detailed_result = {
            "analyses": _result_formOf,
            "lexicon": _result_lookups,
            "input": wordform.decode('utf-8'),
        }

        # TODO: ideally the things here need to be going to an external
        # socket server thing analogous to lookupserv for Oahpa/Sahka.
        # also, for ease of use it needs to be something that the
        # Morphology or XFST or OBT classes spawn and keeps track of
        # For now, just caching things on the hope that this begins to
        # save time.

        # TODO: either clean this up or comment.
        for _r in _result_lookups:
            lemma, pos, tag, _type = _r.get('input')
            paradigm = lang_paradigms.get(pos)
            if tag in lang_baseforms.get(pos):
                _cache_key = hashlib.md5()
                _cache_key.update('generation-%s-' % from_language)
                _cache_key.update(lemma.encode('utf-8'))
                if paradigm:
                    _pos_type = [pos]
                    if _type:
                        _pos_type.append(_type)
                    form_tags = [_pos_type + _t.split('+') for _t in paradigm]
                    _cache_tags = '|'.join(['+'.join(a) for a in form_tags]).encode('utf-8')
                    _cache_key.update(_cache_tags)
                    hexhash = _cache_key.hexdigest()
                    _is_cached = cache.get(hexhash)
                    if _is_cached:
                        _r['paradigms'] = _is_cached
                    else:
                        _generate = morph.generate(lemma, form_tags)
                        cache.set(hexhash, _generate)
                        _r['paradigms'] = _generate
                else:
                    _r['paradigms'] = False
            else:
                _r['paradigms'] = False

        cache.set(cache_key, detailed_result, timeout=5*60)
    else:
        detailed_result = cached_result

    _lookup = detailed_result.get('lexicon')

    if len(_lookup) > 0:
        success = True
        result_lemmas = list(set([entry['input'][0] for entry in detailed_result['lexicon']]))
        _meanings = []
        for lexeme in detailed_result['lexicon']:
            if lexeme['entries']:
                for entry in lexeme['entries']['lookups']:
                    _entry_tx = []
                    for mg in entry['meaningGroups']:
                        _entry_tx.append(mg['translations'])
                    _meanings.append(list(sum(_entry_tx, [])))
        tx_set = '; '.join([', '.join(a) for a in _meanings])
    else:
        success = False
        result_lemmas = ['-']
        tx_set = '-'

    app.logger.info('%s\t%s\t%s\t%s' % (user_input, str(success), ', '.join(result_lemmas), tx_set))

    if format == 'json':
        result = json.dumps({
            "success": True,
            "result": detailed_result
        })
        return result
    elif format == 'html':
        return render_template('word_detail.html', result=detailed_result, user_input=user_input)

@app.route('/kursadict/notify/<from_language>/<to_language>/<wordform>.html',
           methods=['GET'])
@crossdomain(origin='*')
def wordNotification(from_language, to_language, wordform):
    """
    Returns a simplified set of JSON for dictionary, with 'success' to mark
    whether there were no errors. Additional URL parameters are available to
    control the lookup type or whether the lookup is lemmatized before being
    run through the lexicon.

    Path parameters:

        /kursadict/lookup/<from_language>/<to_language>/

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

    success = False
    results = False

    # URL parameters
    lookup_key = user_input = wordform
    lookup_type = False
    lemmatize = True

    if lemmatize and not lookup_type:
        lemm_ = morphologies.get(from_language, False)
        if lemm_:
            lemmatizer = lemm_.lemmatize
        lemmatized_lookup_key = lemmatizer(lookup_key)
    else:
        lemmatized_lookup_key = False

    if lemmatized_lookup_key:
        if not isinstance(lemmatized_lookup_key, list):
            lemmatized_lookup_key = [lemmatized_lookup_key]

        results = []
        for _key in lemmatized_lookup_key:
            result = lookupXML(from_language, to_language,
                               _key, lookup_type)
            result['input'] = _key
            if len(result['lookups']) == 0:
                result['lookups'] = False
            results.append(result)

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)

        if 'error' in result:
            success = False
        else:
            success = True

        if 'lookups' in result:
            if not result['lookups']:
                success = False
    else:

        result = lookupXML(from_language, to_language,
                           lookup_key, lookup_type)
        result['input'] = lookup_key
        if len(result['lookups']) == 0:
            result['lookups'] = False
        results = [result]

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)

        if 'error' in result:
            success = False
        else:
            success = True

        if 'lookups' in result:
            if not result['lookups']:
                success = False

    result_lemmas = set()
    tx_set = set()
    if success:
        for result in results:
            result_lookups = result.get('lookups')
            if result_lookups:
                for lookup in result_lookups:
                    l_left = lookup.get('left')
                    l_right = ', '.join(lookup.get('right'))
                    tx_set.add(l_right)
                    # Reversed lookups return list
                    if isinstance(l_left, list):
                        for _l in l_left:
                            result_lemmas.add(_l)
                    else:
                        result_lemmas.add(lookup.get('left'))

    result_lemmas = ', '.join(list(result_lemmas))
    meanings = '; '.join(list(tx_set))

    app.logger.info('%s\t%s\t%s\t%s' % (user_input, str(success), result_lemmas, meanings))

    return render_template('word_notify.html', result=results, success=success, input=user_input)


##
## Public Docs
##

@app.route('/kursadict/lookup/', methods=['GET'])
def wordLookupDocs():
    from cgi import escape
    _lookup_doc = escape(lookupWord.__doc__)
    return '<html><body><pre>%s</pre></body></html>' % _lookup_doc

@app.route('/kursadict/detail/', methods=['GET'])
def wordDetailDocs():
    from cgi import escape
    _lookup_doc = escape(wordDetail.__doc__)
    return '<html><body><pre>%s</pre></body></html>' % _lookup_doc

##
## Public pages
##
# TODO: config
from collections import OrderedDict

language_pair_descriptions = OrderedDict([
    # pair
   (('sme', 'nob'), {
        # internationalized names (must be unicode type)
        'eng': (u"Northern Sámi", u"Norwegian (Bokmål)"),
        'nob': (u"nordsamisk", u"norsk (bokmål)"),
    }),
   (('nob', 'sme'), {
        'eng': (  u"Norwegian (Bokmål)", u"Northern Sámi"  ),
        'nob': (  u"norsk (bokmål)"    , u"nordsamisk"     ),
    }),

   (('sme', 'fin'), {
        'eng': (  u"Northern Sámi", u"Finnish"  ),
        'nob': (  u"nordsamisk"   , u"finsk"    ),
    }),
   (('fin', 'sme'), {
        'eng': ( u"Finnish" , u"Northern Sámi" ),
        'nob': ( u"finsk"   , u"nordsamisk"    ),
    }),

])

# For direct links, form submission.
@app.route('/kursadict/<_from>/<_to>/', methods=['GET', 'POST'])
def indexWithLangs(_from, _to):
    lookup_val = request.form.get('lookup', False)

    errors = []
    if request.method == 'POST' and lookup_val:
        lemm_ = morphologies.get(_from, False)
        if lemm_:
            lemmatizer = lemm_.lemmatize
            # TODO: what to do if no lemmatizer available
            lemmatized_lookup_key = lemmatizer(lookup_val, split_compounds=True)
        else:
            lemmatized_lookup_key = lookup_val

        if not isinstance(lemmatized_lookup_key, list):
            lemmatized_lookup_key = [lemmatized_lookup_key]

        results = []
        for _key in lemmatized_lookup_key:
            result = lookupXML(_from, _to, _key)
            result['input'] = _key
            if 'error' in result:
                errors.append(result['error'])
                result['lookups'] = False
            elif len(result['lookups']) == 0:
                result['lookups'] = False
            results.append(result)

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)
    else:
        results = False
        user_input = ''

    if len(errors) == 0:
        errors = False
    return render_template('index.html',
                           language_pairs=language_pair_descriptions,
                           _from=_from,
                           _to=_to,
                           user_input=lookup_val,
                           word_searches=results,
                           errors=errors)



@app.route('/kursadict/', methods=['GET'])
def index():
    # TODO: config langauges
    return render_template('index.html', language_pairs=language_pair_descriptions, _from='sme', _to='nob')


##
## Template filters
##

@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

if __name__ == "__main__":
    app.caching_enabled = True
    app.run(debug=True)

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :

