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
TODO: flask wsgi/fcgi thing
TODO: move settings, lookup tool path, fst paths, etc., to somewhere clear

## Todos

TODO: caching

TODO: response for no result

TODO: new xml format from webdicts

/lookup/sme/fin/?lookup=word&analyze=true
  -> ordbok-xml + fst
  1. den du har brukt: ordbok-xml + fst

  TODO: possibility for including tags in response that are associated
        with each lemma analysis


/detailedlookup/sme/fin/wordform.html
/detailedlookup/sme/fin/wordform/json
  2. wordlink og slektningar: ordform-artiklar som html-lenkjer
     - fullform list (main/gt/sme/testing)
       gtsvn/gt/sme/testing/codes/dict/

    viesu (gen of <link>viessu</link>) = hus

    gtsvn/gt/sme/testing/make-gen-dict


TODO: autocomplete from all left language lemmas, build cache and save
      to pickle on each run, then use pickle


## Compiling XML

    java -Xmx2048m -Dfile.encoding=UTF8 net.sf.saxon.Transform \
        -it:main /path/to/gtsvn/words/scripts/collect-dict-parts.xsl \
        inDir=/path/to/gtsvn/words/dicts/smenob/src/ > OUTFILE.xml

"""

import sys

from flask import Flask, request, json
from crossdomain import crossdomain

app = Flask(__name__)

class AppConf(object):
    """ An object for exposing the settings in app.config.yaml in a nice
    objecty way, and validating some of the contents.
    """
    @property
    def dictionaries(self):
        dicts = self.opts.get('Dictionaries')
        language_pairs = {}
        for item in dicts:
            source = item.get('source')
            target = item.get('target')
            path = item.get('path')
            language_pairs[(source, target)] = path
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
        from lxml import etree
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

language_pairs = dict([ (k, XMLDict(filename=v))
                         for k, v in settings.dictionaries.iteritems() ])

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
                fstfile):
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

    return cleanLookups(output)


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

@app.route('/kursadict/test/', methods=['GET'])
def testapp():
    """ A test route to make sure FCGI or WSGI or whatever is working.
    """
    return "omg!"

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

    # URL parameters
    lookup_key = request.args.get('lookup', False)
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

    return json.dumps({
        'result': results,
        'success': success
    })


@app.route('/kursadict/detail/<from_language>/<to_language>/<wordform>/<format>',
           methods=['GET'])
@crossdomain(origin='*')
def wordDetail(from_language, to_language, wordform, format):

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

    detailed_result = {
        "formOf": _result_formOf,
        "lookups": _result_lookups
    }

    # TODO: generate paradigm from lemma and pos
    # TODO: paradigms stored in config file

    # for each result in _result_lookups, add another key with paradigm,
    # so that even words that aren't present in XML get a paradigm
    # generated

    # TODO: HTML and JSON representation switch
    result = json.dumps({
        "success": True,
        "result": detailed_result
    }, indent=4)

    return result



if __name__ == "__main__":
    # NOTE: remove debug later
    app.debug = True
    app.run()

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :

