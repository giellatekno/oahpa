from flask import Flask, request, json
# -*- encoding: utf-8 -*-

"""
A service that provides JSON and RESTful lookups to webdict xml files.

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

Autocomplete for jQuery's autocomplete plugin


## Testing via cURL

    curl -X POST -H "Content-type: application/json" -d ' {"lookup": "fest" } ' http://localhost:5000/lookup/nob/sme/
    curl -X POST -H "Content-type: application/json" -d ' {"lookup": "fest", "type": "startswith" } ' http://localhost:5000/lookup/nob/sme/

## Installing

TODO: document flask installation
TODO: flask wsgi/fcgi thing


## Todos

TODO: autocomplete from all left language lemmas, build cache and save
      to pickle on each run, then use pickle

TODO: caching
"""

app = Flask(__name__)

class XMLDict(object):
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
def lookup(from_language, to_language):
    success = False

    lookup_key = request.json.get('lookup', False)
    lookup_type = request.json.get('type', False)

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

