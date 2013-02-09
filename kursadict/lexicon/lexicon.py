from lxml import etree

##
##  Lexicon
##
##

class LexiconOverrides(object):
    """ Class for collecting functions marked with decorators that
    provide special handling of tags. One class instantiated in
    morphology module: `generation_overrides`.

        @generation_overrides.tag_filter_for_iso('sme')
        def someFunction(form, tags, xml_node):
            ... some processing on tags, may be conditional, etc.
            return form, tags, xml_node

    Each time morphology.generation is run, the args will be passed
    through all of these functions in the order that they were
    registered, allowing for language-specific conditional rules for
    filtering.

    There is also a post-generation tag rewrite decorator registry function
    """

    ##
    ### Here are the functions that apply all the rules
    ##

    def process_prelookups(self, function):
        """ This runs the generator function, and applies all of the
        function contexts to the output. Or in other words, this
        decorator works on the output of the decorated function, but
        also captures the input arguments, making them available to each
        function in the registry.
        """
        def decorate(*args, **kwargs):
            _from = args[0]
            newargs = args
            newkwargs = kwargs
            for f in self.prelookup_processors[_from]:
                newargs, newkwargs = f(*newargs, **newkwargs)
            return function(*newargs, **newkwargs)
        return decorate

    ##
    ### Here are the decorators
    ##

    def pre_lookup_tag_rewrite_for_iso(self, language_iso):
        """ Register a function for a language ISO
        """
        def wrapper(restrictor_function):
            self.prelookup_processors[language_iso]\
                .append(restrictor_function)
            print '%s overrides: lexicon pre-lookup arg rewriter - %s' %\
                  ( language_iso
                  , restrictor_function.__name__
                  )
        return wrapper

    def __init__(self):
        from collections import defaultdict

        self.prelookup_processors = defaultdict(list)

lexicon_overrides = LexiconOverrides()

class XMLDict(object):
    """ XML dictionary class. Initiate with a file path or an already parsed
    tree, exposes methods for searching in XML.

    Entries should be formatted by creating an EntryNodeIterator object,
    which will clean them on iteration.

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
        self.lemmaPOS = etree.XPath(
            './/e[lg/l/text() = $lemma and re:match(lg/l/@pos, $pos, "i")]',
            namespaces={'re':regexpNS})
        self.lemmaPOSAndType = etree.XPath(
            './/e[lg/l/text() = $lemma and re:match(lg/l/@pos, $pos, "i") and lg/l/@type = $_type]',
            namespaces={'re':regexpNS})

    def XPath(self, xpathobj, *args, **kwargs):
        return xpathobj(self.tree, *args, **kwargs)

    def lookupLemmaStartsWith(self, lemma):
        return self.XPath( self.lemmaStartsWith
                         , lemma=lemma
                         )

    def lookupLemma(self, lemma):
        return self.XPath( self.lemma
                         , lemma=lemma
                         )

    def lookupLemmaPOS(self, lemma, pos):
        # Can't insert variables in EXSLT expressions within a compiled
        # xpath statement, so doing this.
        pos = "^%s$" % pos
        return self.XPath( self.lemmaPOS
                         , lemma=lemma
                         , pos=pos
                         )

    def lookupLemmaPOSAndType(self, lemma, pos, _type):
        pos = "^%s$" % pos
        return self.XPath( self.lemmaPOSAndType
                         , lemma=lemma
                         , pos=pos
                         , _type=_type
                         )

class AutocompleteTrie(XMLDict):

    @property
    def allLemmas(self):
        """ Returns iterator for all lemmas.
        """
        return (e.text for e in self.tree.findall('e/lg/l') if e.text)

    def autocomplete(self, query):
        if not self.trie:
            return []
        else:
            return sorted(list(self.trie.autocomplete(query)))

    def __init__(self, *args, **kwargs):
        super(AutocompleteTrie, self).__init__(*args, **kwargs)

        print "* Preparing autocomplete trie..."
        from trie import Trie
        self.trie = Trie()
        try:
            self.trie.update(self.allLemmas)
        except:
            print "Trie processing error"
            print list(self.allLemmas)
            self.trie = False


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


class Lexicon(object):

    def __init__(self, settings):

        language_pairs = dict(
            [ (k, XMLDict(filename=v))
              for k, v in settings.dictionaries.iteritems() ]
        )

        self.lookup = lexicon_overrides.process_prelookups(
            self.lookup
        )

        # reverse_language_pairs = {}

        # for k, v in settings.reversable_dictionaries.iteritems():
        #     _key =      (k[0], k[1])
        #     _reverse  = (k[1], k[0])

        #     has_root = language_pairs.get(_key)

        #     if has_root:
        #         reverse_language_pairs[_reverse] = ReverseLookups(tree=has_root.tree)
        #     else:
        #         reverse_language_pairs[_reverse] = ReverseLookups(filename=v)

        # language_pairs.update(reverse_language_pairs)

        self.language_pairs = language_pairs
        # self.reverse_language_pairs = reverse_language_pairs

        autocomplete_tries = {}
        for k, v in language_pairs.iteritems():
            has_root = language_pairs.get(k)
            if has_root:
                autocomplete_tries[k] = AutocompleteTrie(tree=has_root.tree)

        self.autocomplete_tries = autocomplete_tries

    def get_lookup_type(self, lexicon, lemma, pos, pos_type):
        args = ( bool(lemma)
               , bool(pos)
               , bool(pos_type)
               )

        funcs = { (True, False, False): lexicon.lookupLemma
                , (True, True, False):  lexicon.lookupLemmaPOS
                , (True, True, True):   lexicon.lookupLemmaPOSAndType
                }

        largs = [lemma]
        if pos:
            largs.append(pos)
        if pos_type:
            largs.append(pos_type)

        return funcs.get(args, False), largs

    def lookup(self, _from, _to, lemma,
               pos=False, pos_type=False,
               _format=False):

        _dict = self.language_pairs.get((_from, _to), False)

        if not _dict:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        _lookup_func, largs = self.get_lookup_type(_dict, lemma, pos, pos_type)

        if not _lookup_func:
            raise Exception(
                "Unknown lookup type for lemma: %s, pos: %s, pos_type: %s" %
                ( lemma
                , pos
                , pos_type )
            )

        result = _lookup_func(*largs)

        if len(result) == 0:
            return False

        if _format:
            result = list(_format(result))

        return result

    def lookups(self, _from, _to, lookups, *args, **kwargs):
        from functools import partial

        _look = partial( self.lookup
                       , _from=_from
                       , _to=_to
                       , *args
                       , **kwargs
                       )

        results = zip( lookups
                     , map(lambda x: _look(lemma=x), lookups)
                     )

        success = any([res for l, res in results])

        return results, success

