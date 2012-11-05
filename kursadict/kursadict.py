#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A service that provides JSON and RESTful lookups to webdict xml trie files.

## Configuration

Configuration settings for paths to FSTs, utility programs and
dictionary files must be set in `app.config.yaml`. A sample file is
checked in as `app.config.yaml.in`, so copy this file, edit the settings
and then launch the service.

## Endpints

### /lookup/<from_language>/<to_language>/

    POST JSON format:

        Object object:
           {"lookup": "fest"}

        Optional parameter: type
           {"lookup": "fest", "type": "startswith"}

        Optional parameter: lemmatize
           {"lookup": "geavaheaddjit", "lemmatize": true}

           Run lookup string through lemmatizer, and look those results up in
           XML lexicon files.

### /auto/<language>

Autocomplete for jQuery's autocomplete plugin, available from:
  http://jqueryui.com/autocomplete/

TODO: return array of lemmas formatted such:

    [ { label: "Choice1", value: "value1" }, ... ]

## Testing via cURL

    curl -X POST -H "Content-type: application/json" \
         -d ' {"lookup": "fest" } ' \
         http://localhost:5000/lookup/nob/sme/

    curl -X POST -H "Content-type: application/json" \
         -d ' {"lookup": "fest", "type": "startswith" } \
         ' http://localhost:5000/lookup/nob/sme/

## Installing

TODO: document flask installation
TODO: flask wsgi/fcgi thing
TODO: move settings, lookup tool path, fst paths, etc., to somewhere clear

## Todos

TODO: autocomplete from all left language lemmas, build cache and save
      to pickle on each run, then use pickle

TODO: caching

TODO: response for no result

"""

import sys

from flask import Flask, request, json
from crossdomain import crossdomain

app = Flask(__name__)

class AppConf(object):
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
        fsts = self.opts.get('FSTs')
        for k, v in fsts.iteritems():
            try:
                open(v, 'r')
            except IOError:
                sys.exit('FST for %s, %s, does not exist. Check path in app.config.yaml.' % (k, v))
        return fsts

    @property
    def lookup_command(self):
        apps = self.opts.get('Utilities')
        cmd = apps.get('lookup_path')
        try:
            open(cmd, 'r')
        except IOError:
            sys.exit('Lookup utility (%s) does not exist' % cmd)
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

class XMLDict(object):
    """ XML dictionary class. Initiate with a file path, exposes methods
    for searching in XML.
    """
    def __init__(self, filename):
        from lxml import etree
        self.tree = etree.parse(filename)

    def lookupLemmaStartsWith(self, lemma):
        def clean_node(node):
            left = node.find('l')
            left_text = left.text
            left_pos = left.find('s').get('n')
            right_text = node.find('r').text
            return {'left': left_text, 'pos': left_pos, 'right': right_text}
        _xpath = './/w[starts-with(@v, "%s")]' % lemma
        w_nodes = self.tree.xpath(_xpath)
        return map(clean_node, w_nodes)

    def lookupLemma(self, lemma):
        def clean_node(node):
            left = node.find('l')
            left_text = left.text
            left_pos = left.find('s').get('n')
            right_text = node.find('r').text
            return {'left': left_text, 'pos': left_pos, 'right': right_text}
        w_nodes = self.tree.findall('.//w[@v="%s"]' % lemma)
        return map(clean_node, w_nodes)

_language_pairs = settings.dictionaries
language_pairs = dict([(k, XMLDict(filename=v)) for k, v in _language_pairs.iteritems()])

def lookupXML(_from, _to, lookup, lookup_type=False):
    _dict = language_pairs.get((_from, _to), False)
    if _dict:
        if lookup_type:
            if lookup_type == 'startswith':
                return {'lookups': _dict.lookupLemmaStartsWith(lookup)}
        return {'lookups': _dict.lookupLemma(lookup)}

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


def lemmatizer(language, lookup):
    fstfile = FSTs.get(language, False)
    if not fstfile:
        print "No FST for language."
        return False

    if isinstance(lookup, unicode):
        lookup = lookup.encode('utf-8')
    results = lookupInFST([lookup], fstfile)

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
    return "omg!"

@app.route('/kursadict/lookup/<from_language>/<to_language>/',
           methods=['GET'])
@crossdomain(origin='*')
def lookupWord(from_language, to_language):
    success = False
    data = False
    lemmatize = False

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


if __name__ == "__main__":
    # NOTE: remove debug later
    app.debug = True
    app.run()

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :

