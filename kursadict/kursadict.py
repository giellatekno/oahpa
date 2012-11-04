from flask import Flask, request, json
# -*- encoding: utf-8 -*-
"""
A service that provides JSON and RESTful lookups to webdict xml trie files.

## Endpints

### /lookup/<from_language>/<to_language>/

    POST JSON format: 
    
        Object object: 
           {"lookup": "fest"}

        Optional parameter: type
           {"lookup": "fest", "type": "startswith"}

        Optional parameter: fst lookup first
           # TODO: grab lookups from lookupserver, then return results

### /auto/<language>

Autocomplete for jQuery's autocomplete plugin, available from: http://jqueryui.com/autocomplete/

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


## Todos

TODO: autocomplete from all left language lemmas, build cache and save
      to pickle on each run, then use pickle

TODO: caching
"""
from crossdomain import crossdomain
app = Flask(__name__)

class XMLDict(object):
    # TODO: reverse option, and do lookups on 'r' side instead.
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

language_pairs = {
    ('nob', 'sme'): XMLDict(filename='nob-sme-lr-trie.xml'),
    # TODO: ('fin', 'sme'): XMLDict(filename='nob-sme-lr-trie.xml'),
    # TODO: ('sme', 'nob'): XMLDict(filename='nob-sme-lr-trie.xml',
    #                               reverse=True),
}

def lookupXML(_from, _to, lookup, lookup_type=False):
    _dict = language_pairs.get((_from, _to), False)
    if _dict:
        if lookup_type:
            if lookup_type == 'startswith':
                return {'lookups': _dict.lookupLemmaStartsWith(lookup)}
        return {'lookups': _dict.lookupLemma(lookup)}

    else:
        return {'error': "Unknown language pair"}

@app.route('/lookup/<from_language>/<to_language>/', methods=['GET', 'POST'])
@crossdomain(origin='*')
def lookup(from_language, to_language):
    success = False
    data = False

    if request.method == "POST":
        if request.json:
            data = request.json
        # Mimetype not sent correctly
        if request.form:
            data = json.loads(request.form.keys()[0])

    if data:
        lookup_key = data.get('lookup', False)
        lookup_type = data.get('type', False)

    if lookup_key:
        result = lookupXML(from_language, to_language, lookup_key, lookup_type)
        if 'error' in result:
            success = False
        else:
            success = True

    return json.dumps({
        'result': result,
        'success': success
    })


if __name__ == "__main__":
    # NOTE: remove debug later
    app.debug = True
    app.run()

