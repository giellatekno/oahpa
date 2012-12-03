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

TODO: for now the reverse versions of the dictionaries are not ready, so
we're using the same file but just different xpath lookups. it may be
that some dictionaries don't really work well with this, so we'll need
to develop a config option for marking them as reversable or not.

    tag: #reversed

## Compiling XML

    java -Xmx2048m -Dfile.encoding=UTF8 net.sf.saxon.Transform \
        -it:main /path/to/gtsvn/words/scripts/collect-dict-parts.xsl \
        inDir=/path/to/gtsvn/words/dicts/smenob/src/ > OUTFILE.xml

"""

import sys
import logging
import urllib

from lxml import etree
from flask import Flask, request, json, render_template, Markup
from werkzeug.contrib.cache import SimpleCache
from crossdomain import crossdomain

cache = SimpleCache()
app = Flask(__name__, 
    static_url_path='/kursadict/static',)

useLogFile = logging.FileHandler('user_log.txt')
app.logger.addHandler(useLogFile)

class AppConf(object):
    """ An object for exposing the settings in app.config.yaml in a nice
    objecty way, and validating some of the contents.
    """
    @property
    def baseforms(self):
        if self._baseforms:
            return self._baseforms

        lang_baseforms = self.opts.get('Baseforms')

        self._baseforms = lang_baseforms
        return self._baseforms

    @property
    def paradigms(self):
        if self._paradigms:
            return self._paradigms

        lang_paradigms = self.opts.get('Paradigms')

        self._paradigms = lang_paradigms
        return self._paradigms
        
    @property
    def reversable_dictionaries(self):
        if self._reversable_dictionaries:
            return self._reversable_dictionaries

        def isReversable(d):
            if d.get('reversable', False):
                return d

        dicts = filter(isReversable, self.opts.get('Dictionaries'))
        language_pairs = {}
        for item in dicts:
            
            source = item.get('source')
            target = item.get('target')
            path = item.get('path')
            language_pairs[(source, target)] = path

        self._reversable_dictionaries = language_pairs
        return language_pairs

    @property
    def dictionaries(self):
        if self._dictionaries:
            return self._dictionaries

        dicts = self.opts.get('Dictionaries')
        language_pairs = {}
        for item in dicts:
            source = item.get('source')
            target = item.get('target')
            path = item.get('path')
            language_pairs[(source, target)] = path

        self._dictionaries = language_pairs
        return language_pairs

    @property
    def FSTs(self):
        """ Iterate and check that FSTs exist """
        fsts = self.opts.get('FSTs')
        for k, v in fsts.iteritems():
            try:
                open(v, 'r')
            except IOError:
                sys.exit('FST for %s, %s, does not exist. Check path in app.config.yaml.' % (k, v))
        return fsts

    @property
    def lookup_command(self):
        """ Check that the lookup command is executable and user has
        permissions to execute. """
        import os
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        
        apps = self.opts.get('Utilities')
        cmd = apps.get('lookup_path')
        
        if not is_exe(cmd):
            sys.exit('Lookup utility (%s) does not exist, \
                      or you have no exec permissions' % cmd)
        cmd_opts = apps.get('lookup_opts', False)
        if cmd_opts:
            cmd += ' ' + cmd_opts
        return cmd

    def __init__(self):
        self._dictionaries            = False
        self._reversable_dictionaries = False
        self._paradigms               = False
        self._baseforms               = False

        import yaml
        with open('app.config.yaml', 'r') as F:
            config = yaml.load(F)
        self.opts = config
        
settings = AppConf()

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
            self.tree = etree.parse(filename)
        else:
            self.tree = tree

    def cleanEntry(self, e):
        l = e.find('lg/l')
        left_text = l.text
        left_pos = l.get('pos')
        ts = e.findall('mg/tg/t')
        right_text = [t.text for t in ts]
        return {'left': left_text, 'pos': left_pos, 'right': right_text}

    def XPath(self, query):
        return map(self.cleanEntry, self.tree.xpath(query))

    def lookupLemmaStartsWith(self, lemma):
        _xpath = './/e[starts-with(lg/l/text(), "%s")]' % lemma
        return self.XPath(_xpath)

    def lookupLemma(self, lemma):
        _xpath = './/e[lg/l/text() = "%s"]' % lemma
        return self.XPath(_xpath)

    def lookupLemmaPOS(self, lemma, pos):
        _xpath = './/e[lg/l/text() = "%s" and lg/l/@pos = "%s"]' % (lemma, pos.lower())
        return self.XPath(_xpath)

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
            'meaningGroups': meaningGroups

        }

class ReverseLookups(XMLDict):
    """
    NOTE: #reversed

    1. use only entries that have the attribute usage="vd" at entry
    level

    2. don't use entries with reverse="no" at entry level

    3. search by e/mg/tg/t/text() instead of /e/lg/l/text()
    """

    def cleanEntry(self, e):
        """ TODO: need to reverse this
        """
        # print etree.tostring(e, pretty_print=True)
        l = e.find('lg/l')
        left_text = l.text
        left_pos = l.get('pos')
        ts = e.findall('mg/tg/t')
        right_text = [t.text for t in ts]

        return {'left': left_text, 'pos': left_pos, 'right': right_text}

    def lookupLemmaStartsWith(self, lemma):
        _xpath = './/e[mg/tg/t/starts-with(text(), "%s")]' % lemma
        return self.XPath(_xpath)

    def lookupLemma(self, lemma):
        _xpath = './/e[mg/tg/t/text() = "%s" and @usage = "vd" and not(@reverse)]'
        return self.XPath(_xpath % lemma)

    def lookupLemmaPOS(self, lemma, pos):
        _xpath = './/e[mg/tg/t/text() = "%s" and @usage = "vd" and not(@reverse) and mg/tg/t/@pos = "%s"]'
        _xpath = _xpath % (lemma, pos.lower())
        return self.XPath(_xpath)


language_pairs = dict([ (k, XMLDict(filename=v))
                         for k, v in settings.dictionaries.iteritems() ])

# NOTE: #reversed
reverse_language_pairs = dict([ ((k[1], k[0]), ReverseLookups(filename=v))
                              for k, v in settings.reversable_dictionaries.iteritems() ])

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


def detailedLookupXML(_from, _to, lookup, pos):
    lexicon = language_pairs.get((_from, _to), False)
    # wrap in mixin for detailed results
    detailed_tree = DetailedEntries(tree=lexicon.tree)

    if lexicon and detailed_tree:
        # TODO: include PoS
        return {'lookups': detailed_tree.lookupLemmaPOS(lookup, pos)}
    else:
        return {'error': "Unknown language pair"}

##
##  Lemmatization
##
##

LOOKUP_TOOL = settings.lookup_command

FSTs = settings.FSTs

def cleanLookups(lookup_string):
    """
        Clean XFST lookup text into

        [('keenaa', ['keen+V+1Sg+Ind+Pres', 'keen+V+3SgM+Ind+Pres']),
         ('keentaa', ['keen+V+2Sg+Ind+Pres', 'keen+V+3SgF+Ind+Pres'])]

    """

    analysis_chunks = [a for a in lookup_string.split('\n\n') if a.strip()]

    cleaned = []
    for chunk in analysis_chunks:
        lemmas = []
        analyses = []

        for part in chunk.split('\n'):
            lemma, _, analysis = part.partition('\t')
            lemmas.append(lemma)
            analyses.append(analysis)

        lemma = list(set(lemmas))[0]

        append_ = (lemma, analyses)

        cleaned.append(append_)

    return cleaned


def lookupInFST(lookups_list,
                fstfile,
                decodeOutput=False):
    """ Send the lookup string(s) to an external FST process. Kill the process
    after 5 seconds if no response seems to be coming.
    """

    import subprocess
    from threading import Timer

    lookup_string = '\n'.join(lookups_list)

    gen_norm_command = ' '.join([LOOKUP_TOOL, fstfile])
    gen_norm_command = gen_norm_command.split(' ')

    lookup_proc = subprocess.Popen(gen_norm_command,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    def kill_proc(proc=lookup_proc):
        try:
            proc.kill()
            _cmdError = ''.join(gen_norm_command)
            raise Http404("Process for %s took too long." % _cmdError)
        except OSError:
            pass
        return

    t = Timer(5, kill_proc)
    t.start()

    output, err = lookup_proc.communicate(lookup_string)

    if decodeOutput:
        output = output.decode('utf-8')

    return cleanLookups(output)

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

def generateFromList(language_iso, lookup_strings):
    fstfile = FSTs.get(language_iso + '_gen', False)
    lookup_strings = map(encodeOrFail, lookup_strings)
    if not fstfile:
        print "No FST for language."
        return False

    results = lookupInFST(lookup_strings, fstfile, decodeOutput=True)

    return results


def lemmatizeWithTags(language_iso, lookup_string):
    """ Given a language code and lookup string, returns a list of lemma
    strings, repeats will not be repeated.
    """
    fstfile = FSTs.get(language_iso, False)
    if not fstfile:
        print "No FST for language."
        return False

    if isinstance(lookup_string, unicode):
        lookup_string = lookup_string.encode('utf-8')

    results = lookupInFST([lookup_string], fstfile)

    lemmas = dict()

    for _input, analyses in results:
        for analysis in analyses:
            lemma, _, tag = analysis.partition('+')
            if not lemma.decode('utf-8') in lemmas:
                lemmas[lemma.decode('utf-8')] = set([tag])
            else:
                lemmas[lemma.decode('utf-8')].add(tag)

    return lemmas

def lemmatizer(language_iso, lookup_string):
    """ Given a language code and lookup string, returns a list of lemma
    strings, repeats will not be repeated.
    """
    fstfile = FSTs.get(language_iso, False)
    if not fstfile:
        print "No FST for language."
        return False

    if isinstance(lookup_string, unicode):
        lookup_string = lookup_string.encode('utf-8')

    results = lookupInFST([lookup_string], fstfile)

    lemmas = set()

    for _input, analyses in results:
        for analysis in analyses:
            lemma, _, tag = analysis.partition('+')
            lemmas.add(lemma.decode('utf-8'))

    return list(lemmas)


##
##  Endpoints
##
##
@app.route('/kursadict/testreverse/', methods=['GET'])
def reverseLookupTest():
    print lookupXML('nob', 'sme', 'gate')
    return ""

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
        lookup_key = lemmatizer(from_language, lookup_key)

    if lookup_key:
        if not isinstance(lookup_key, list):
            lookup_key = [lookup_key]

        results = []
        for _key in lookup_key:
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

    result_lemmas = set()
    if success:
        for result in results:
            result_lookups = result.get('lookups')
            if result_lookups:
                for lookup in result_lookups:
                    result_lemmas.add(lookup.get('left'))
    result_lemmas = list(result_lemmas)

    app.logger.info('%s\t%s\t%s' % (user_input, str(success), ', '.join(result_lemmas)))

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

    cache_key = '/detail/%s/%s/%s.%s' % (from_language, to_language, wordform, format)
    wordform = wordform.encode('utf-8')

    if app.caching_enabled:
        cached_result = cache.get(cache_key)
    else:
        cached_result = None

    if cached_result is None:

        lang_paradigms = settings.paradigms.get('sme')
        lang_baseforms = settings.baseforms.get('sme')
        # All lookups in XML must go through analyzer, because we need POS
        # info for a good lookup.
        analyzed = lemmatizeWithTags(from_language, wordform)

        # Collect lemmas and tags
        _result_formOf = []
        for form, tags in analyzed.iteritems():
            for tag in tags:
                pos, _, rest = tag.partition('+')
                _result_formOf.append((form, pos, tag))

        # Now collect XML lookups
        _result_lookups = []
        for lemma, pos, tag in _result_formOf:

            # Only look up word when there is a baseform
            paradigm = lang_paradigms.get(pos)
            if tag in lang_baseforms.get(pos):
                xml_result = detailedLookupXML(from_language,
                                               to_language,
                                               lemma,
                                               pos)

                if len(xml_result['lookups']) == 0:
                    xml_result = False

                _result_lookups.append({
                    'lookups': xml_result,
                    'input': (lemma, pos, tag)
                })
            else:
                continue

        detailed_result = {
            "formOf": _result_formOf,
            "lookups": _result_lookups,
            "input": wordform.decode('utf-8'),
        }

        # TODO: generate paradigm from lemma and pos
        for _r in _result_lookups:
            lemma, pos, tag = _r.get('input')
            paradigm = lang_paradigms.get(pos)
            if tag in lang_baseforms.get(pos):
                generate_strings = ['%s+%s' % (lemma, _t) for _t in paradigm]
                _r['paradigms'] = generateFromList(from_language, generate_strings)
            else:
                _r['paradigms'] = False


        cache.set(cache_key, detailed_result, timeout=5*60)
    else:
        detailed_result = cached_result

    # TODO: log result
    # result_lemmas = set()
    # if success:
    #     for result in results:
    #         for lookup in result.get('lookups', []):
    #             result_lemmas.add(lookup.get('left'))
    # result_lemmas = list(result_lemmas)

    # app.logger.info('%s\t%s\t%s' % (user_input, str(success), ', '.join(result_lemmas)))

    if format == 'json':
        result = json.dumps({
            "success": True,
            "result": detailed_result
        }, indent=4)
        return result
    elif format == 'html':
        return render_template('word_detail.html', result=detailed_result)

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
    app.debug = True
    app.caching_enabled = True
    app.run()

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :

