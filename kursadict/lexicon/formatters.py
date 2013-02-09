
def flatten(_list):
    return list(sum(_list, []))

class EntryNodeIterator(object):
    """ A class for iterating through the result of an LXML XPath query,
    while cleaning the nodes into a more usable format.

    .clean() is where most of the magic happens, so if new formats are
    needed, just override this.

    """

    def l_node(self, entry):
        l = entry.find('lg/l')
        lemma = l.text
        pos = l.get('pos')
        context = l.get('context')
        type = l.get('type')
        hid = l.get('hid')
        if context == None:
            context = False
        if type == None:
            type = False
        if hid == None:
            hid = False

        return lemma, pos, context, type, hid

    def tg_nodes(self, entry):
        target_lang = self.query_kwargs.get('target_lang', False)

        if target_lang:
            ts = entry.xpath("mg/tg[@xml:lang='%s']/t" % target_lang)
            tgs = entry.xpath("mg/tg[@xml:lang='%s']" % target_lang)

        if not target_lang or len(tgs) == 0:
            ts = entry.findall('mg/tg/t')
            tgs = entry.findall('mg/tg')

        return tgs, ts

    def examples(self, tg):
        _ex = [ (xg.find('x').text, xg.find('xt').text)
                for xg in tg.findall('xg') ]
        if len(_ex) == 0:
            return False
        else:
            return _ex

    def find_translation_text(self, tg):

        def orFalse(l):
            if len(l) > 0:
                return l[0]
            else:
                return False

        text = False
        re = tg.find('re')
        te = tg.find('te')
        tf = tg.find('tf')

        te_text = ''
        re_text = ''
        tf_text = ''

        if te is not None:      te_text = te.text
        if re is not None:      re_text = re.text
        if tf is not None:      tf_text = tf.text

        tx = tg.findall('t')

        link = True

        if not tx:
            if te_text:
                text, te_text = [te_text], ''
            elif re_text:
                text, re_text = [re_text], ''
            elif tf_text:
                text, tf_text = [tf_text], ''
        else:
            text = [_tx.text for _tx in tx]

        lang = tg.xpath('@xml:lang')

        annotations = [a for a in [te_text, re_text, tf_text] if a.strip()]

        return text, annotations, lang

    def __init__(self, nodes, *query_args, **query_kwargs):
        if not nodes or len(nodes) == 0:
            self.nodes = []
        else:
            self.nodes = nodes
        self.query_args = query_args
        self.query_kwargs = query_kwargs

    def __iter__(self):
        for node in self.nodes:
            yield self.clean(node)

class SimpleJSON(EntryNodeIterator):
    """ A simple JSON-ready format for /lookups/
    """

    def clean(self, e):
        lemma, lemma_pos, lemma_context, _, lemma_hid = self.l_node(e)
        tgs, ts = self.tg_nodes(e)

        translations = map(self.find_translation_text, tgs)
        right_text = flatten([a for a, b, c in translations])
        right_langs = flatten([c for a, b, c in translations])

        return { 'left': lemma
               , 'context': lemma_context
               , 'pos': lemma_pos
               , 'right': right_text
               , 'lang': right_langs
               , 'hid': lemma_hid
               }


class DetailedFormat(EntryNodeIterator):
    def clean(self, e):
        lemma, lemma_pos, lemma_context, lemma_type, lemma_hid = self.l_node(e)
        tgs, ts = self.tg_nodes(e)

        meaningGroups = []
        for tg in tgs:
            text, annotations, lang = self.find_translation_text(tg)
            if isinstance(text, list):
                text = ', '.join(text)
            if isinstance(annotations, list):
                annotations = ', '.join(annotations)
            meaningGroups.append(
                { 'annotations': annotations
                , 'translations': text
                , 'examples': self.examples(tg)
                , 'language': lang
                }
            )

        # Make our own hash, 'cause lxml won't
        entry_hash = [ unicode(lemma)
                     , unicode(lemma_context)
                     , unicode(lemma_pos)
                     , ','.join(sorted([t['translations'] for t in meaningGroups]))
                     ]
        entry_hash = str('-'.join(entry_hash).__hash__())

        return { 'lemma': lemma
               , 'lemma_context': lemma_context
               , 'pos': lemma_pos
               , 'hid': lemma_hid
               , 'meaningGroups': meaningGroups
               , 'type': lemma_type
               , 'node': e
               , 'entry_hash': entry_hash
               }

class FrontPageFormat(EntryNodeIterator):

    def clean(self, e):
        lemma, lemma_pos, lemma_context, lemma_type, lemma_hid = self.l_node(e)
        tgs, ts = self.tg_nodes(e)

        right_nodes = []
        right_langs = []
        for tg in tgs:
            text, annotations, lang = self.find_translation_text(tg)
            right_langs.append(lang)
            link = True
            if isinstance(text, list):
                if len(text) > 1:
                    link = False
                text = ', '.join(text)
            else:
                link = True

            right_nodes.append({ 'tx': text
                               , 're': annotations
                               , 'link': link
                               , 'examples': self.examples(tg)
                               })

        # Make our own hash, 'cause lxml won't
        entry_hash = [ unicode(lemma)
                     , unicode(lemma_context)
                     , unicode(lemma_pos)
                     , ','.join(sorted([t['tx'] for t in right_nodes]))
                     ]
        entry_hash = str('-'.join(entry_hash).__hash__())

        return { 'left': lemma
               , 'context': lemma_context
               , 'pos': lemma_pos
               , 'right': right_nodes
               , 'lang': right_langs
               , 'hid': lemma_hid
               , 'entry_hash': entry_hash
               }
