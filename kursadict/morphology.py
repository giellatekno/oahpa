#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Morphological tools
"""

class Tagset(object):
    def __init__(self, name, members):
        self.name = name
        self.members = members
    def __str__(self):
        return '<Tagset: "%s">' % self.name

class Tagsets(object):
    def __init__(self, set_definitions):
        self.sets = {}
        self.set_definitions = set_definitions
        self.createTagSets()
    def createTagSets(self):
        for name, tags in self.set_definitions.iteritems():
            tagset = Tagset(name, tags)
            self.set(name, tagset)
    def get(self, name):
        return self.sets.get(name, False)
    def __getitem__(self, key):
        return self.get(key)
    def set(self, name, tagset):
        self.sets[name] = tagset

class Tag(object):
    """ A model for tags. Can be used as an iterator, as well.

    >>> for part in Tag('N+G3+Sg+Ill', '+'):
    >>>     print part

    Also, indexing is the same as Tag.getTagByTagset()

    >>> _type = Tagset('type', ['G3', 'NomAg'])
    >>> _case = Tagset('case', ['Nom', 'Ill', 'Loc'])
    >>> _ng3illsg = Tag('N+G3+Sg+Ill', '+')
    >>> _ng3illsg[_type]
    'G3'
    >>> _ng3illsg[_case]
    'Ill'

    TODO: maybe also contains for tag parts and tagsets

    TODO: begin integrating Tag and Tagsets into morphology code below,
    will help when generalizing the lexicon-morphology 'type' and 'pos'
    stuff. E.g., in `sme`, we look up words by 'pos' and 'type' when it
    exists, but in other languages this will be different. As such, we
    will need `Tag`, and `Tagset` and `Tagsets` to mitigate this.

    Also, will need some sort of lexicon lookup definition in configs,
    to describe how to bring these items together.
    """
    def __init__(self, string, sep):
        self.tag_string = string
        self.sep = sep
        self.parts = self.tag_string.split(sep)
    def __getitem__(self, b):
        """ Overloading the xor operator to produce the tag piece that
        belongs to a given tagset. """
        if not isinstance(b, Tagset):
            raise TypeError("Second value must be a tagset")
        return self.getTagByTagset(b)
    def __iter__(self):
        for x in self.parts:
            yield x
    def __str__(self):
        return '<Tag: %s>' % self.sep.join(self.parts)
    def getTagByTagset(self, tagset):
        for p in self.parts:
            if p in tagset.members:
                return p
    def splitByTagset(self, tagset):
        """
        >>> tagset = Tagset('compound', ['Cmp#'])
        >>> tag = Tag('N+Cmp#+N+Sg+Nom')
        >>> tag.splitByTagset(tagset)
        [<Tag: N>, <Tag: N+Sg+Nom>]
        """
        raise NotImplementedError

class XFST(object):

    def splitTagByCompound(self, analysis):
        _cmp =  self.options.get('compoundBoundary', False)
        if _cmp:
            return analysis.split(_cmp)
        else:
            return [analysis]

    def clean(self, _output):
        """
            Clean XFST lookup text into

            [('keenaa', ['keen+V+1Sg+Ind+Pres', 'keen+V+3SgM+Ind+Pres']),
             ('keentaa', ['keen+V+2Sg+Ind+Pres', 'keen+V+3SgF+Ind+Pres'])]

        """

        analysis_chunks = [a for a in _output.split('\n\n') if a.strip()]

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

    # TODO: need to cache eeeeeeeeeeeeverything.
    def _exec(self, _input, cmd, timeout=5):
        """ Execute a process, but kill it after 5 seconds. Generally
        we expect small things here, not big things.
        """
        import subprocess
        from threading import Timer

        try:     _input = _input.encode('utf-8')
        except:  pass

        lookup_proc = subprocess.Popen(cmd.split(' '),
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

        def kill_proc(proc=lookup_proc):
            try:
                proc.kill()
                raise Exception("Process for %s took too long." % cmd)
            except OSError:
                pass
            return

        if not timeout:
            t = Timer(5, kill_proc)
            t.start()

        output, err = lookup_proc.communicate(_input)

        if output:
            try:     output = output.decode('utf-8')
            except:  pass

        if err:
            try:     err = err.decode('utf-8')
            except:  pass

        return (output, err)

    def __init__(self, lookup_tool, fst_file, ifst_file=False, options={}):
        self.cmd = "%s -flags mbTT %s" % (lookup_tool, fst_file)
        self.options = options

        if ifst_file:
            self.icmd = "%s -flags mbTT %s" % (lookup_tool, ifst_file)
        else:
            self.icmd = False

    def __rshift__(left, right):
        right.tool = left
        left.logger = right.logger
        return right

    def lookup(self, lookups_list):
        lookup_string = '\n'.join(lookups_list)
        output, err = self._exec(lookup_string, cmd=self.cmd)
        if len(output) == 0 and len(err) > 0:
            name = self.__class__.__name__
            msg = """%(name)s: %(err)s""" % locals()
            self.logger.error(msg.strip())
        return self.clean(output)

    def inverselookup(self, lemma, tags):

        if not self.icmd:
            print >> sys.stderr, " * Inverse lookups not available."
            return False

        lookups_list = []
        for tag in tags:
            lookups_list.append(self.formatTag([lemma] + tag, inverse=True))
        lookup_string = '\n'.join(lookups_list)
        output, err = self._exec(lookup_string, cmd=self.icmd)
        return self.clean(output)

    def tagUnknown(self, analysis):
        if '+?' in analysis:
            return True
        else:
            return False

    def formatTag(self, parts, inverse=False):
        if inverse:
            delim = self.options.get('inverse_tagsep',
                self.options.get('tagsep', '+'))
        else:
            delim = self.options.get('tagsep', '+')
        return delim.join(parts)

    def splitAnalysis(self, analysis, inverse=False):
        """ u'lemma+Tag+Tag+Tag' -> [u'lemma', u'Tag', u'Tag', u'Tag'] """
        if inverse:
            delim = self.options.get('inverse_tagsep',
                self.options.get('tagsep', '+'))
        else:
            delim = self.options.get('tagsep', '+')

        return analysis.split(delim)

class OBT(XFST):
    """ TODO: this is almost like CG, so separate out those things if necessary.
    """

    def clean(self, _output):
        """ Clean CG lookup text into

            [('keenaa', ['keen+V+1Sg+Ind+Pres', 'keen+V+3SgM+Ind+Pres']),
             ('keentaa', ['keen+V+2Sg+Ind+Pres', 'keen+V+3SgF+Ind+Pres'])]

        """

        analysis_chunks = []

        chunk = []
        for line in _output.splitlines():

            if line.startswith('"<'):
                if len(chunk) > 0:
                    analysis_chunks.append(chunk)
                chunk = [line]
                continue
            elif line.startswith("\t\""):
                chunk.append(line.strip())
        else:
            analysis_chunks.append(chunk)

        cleaned = []
        for chunk in analysis_chunks:
            form, analyses = chunk[0], chunk[1::]

            lemmas = []
            tags = []
            for part in analyses:
                tagparts = part.split(' ')
                lemma = tagparts[0]
                lemma = lemma.replace('"', '')
                lemmas.append(lemma)
                tags.append(' '.join([lemma] + tagparts[1::]))

            lemma = list(set(lemmas))[0]

            form = form[2:len(form)-2]
            append_ = (form, tags)

            cleaned.append(append_)

        return cleaned

    def splitAnalysis(self, analysis):
        return analysis.split(' ')

    def __init__(self, lookup_tool, options={}):
        self.cmd = lookup_tool
        self.options = options


class Morphology(object):

    def cleanTag(self, tag):
        exclusions = [
            'Ani', 'Body', 'Build', 'Clth', 'Edu', 'Event', 'Fem',
            'Food', 'Group', 'Hum', 'Mal', 'Measr', 'Obj', 'Org',
            'Plant', 'Plc', 'Route', 'Sur', 'Time', 'Txt', 'Veh', 'Wpn',
            'Wthr', 'Allegro', 'v1', 'v2', 'v3', 'v4',
        ]
        cleaned = []
        for p in tag:
            if p in exclusions:
                continue
            cleaned.append(p)
        return cleaned

    def generate(self, lemma, tagsets):
        """ Run the lookup command, parse output into
            [(lemma, ['Verb', 'Inf'], ['form1', 'form2'])]
        """
        res = self.tool.inverselookup(lemma, tagsets)
        reformatted = []
        for tag, forms in res:
            unknown = False
            for f in forms:
                # TODO: how does OBT handle unknown?
                if '+?' in f:
                    unknown = True
                    msg = self.tool.__class__.__name__ + ': ' + \
                         tag + '\t' + '|'.join(forms)
                    self.tool.logger.error(msg)

            if not unknown:
                parts = self.tool.splitAnalysis(tag, inverse=True)
                lemma = parts[0]
                tag = self.cleanTag(parts[1::])
                reformatted.append((lemma, tag, forms))
            else:
                parts = self.tool.splitAnalysis(tag, inverse=True)
                lemma = parts[0]
                tag = parts[1::]
                forms = False
                reformatted.append((lemma, tag, forms))

        return reformatted


    def lemmatize(self, form, split_compounds=False,
                  non_compound_only=False, no_derivations=False, output_tags=False):
        """ For a wordform, return a list of lemmas
        """
        class Lemma(object):
            def __key(lem_obj):
                return (lem_obj.lemma, lem_obj.pos, self.tool.formatTag(lem_obj.tag))
            def __eq__(x, y):
                return x.__key() == y.__key()
            def __hash__(lem_obj):
                return hash(lem_obj.__key())
            def __unicode__(lem_obj):
                return lem_obj.lemma
            def __repr__(lem_obj):
                _lem, _pos, _tag = lem_obj.__key()
                return '<Lemma: %s, %s, %s>' % (_lem, _pos, _tag)
            def __init__(lem_obj, lemma, pos, tag, _input=False):
                lem_obj.lemma = lemma
                lem_obj.pos = pos
                lem_obj.tag = tag
                lem_obj.input = _input

        def remove_compound_analyses(_a):
            _cmp =  self.tool.options.get('compoundBoundary', False)
            if not _cmp:
                return True
            if _cmp in _a:
                return False
            else:
                return True

        def remove_derivations(_a):
            _der = self.tool.options.get('derivationMarker', False)
            if not _der:
                return True
            if _der in _a:
                return False
            else:
                return True

        def maybe_filter(function, iterable):
            result = filter(function, iterable)
            if len(result) > 0:
                return result
            else:
                return iterable

        lookups = self.tool.lookup([form])

        lemmas = set()

        for _form, analyses in lookups:

            if non_compound_only:
                analyses = maybe_filter(remove_compound_analyses, analyses)

            if no_derivations:
                analyses = maybe_filter(remove_derivations, analyses)

            if split_compounds:
                analyses = sum( map(self.tool.splitTagByCompound, analyses)
                              , []
                              )

            for analysis in analyses:
                _an_parts = self.tool.splitAnalysis(analysis)
                _lem, _pos, _analysis = _an_parts[0], _an_parts[1], _an_parts[2::]
                lem = Lemma(_lem, _pos, _analysis, form)
                lemmas.add(lem)

        return list(lemmas)

    def analyze(self, form, split_compounds=False):
        """ For a wordform, return a list of lemmas and analyses
            Return in form of:
            [(form, lemma, ['Verb', 'Inf']),
             (form, lemma, ['Verb', 'Inf']),
            ]
        """
        lookups = self.tool.lookup([form])

        unknown = False
        cleaned = []
        if split_compounds:
            for _input, tags in lookups:
                for tag in tags:
                    # TODO: how does OBT handle unknown?
                    if '+?' in tag:
                        unknown = True
                        cleaned.append((_input, '?', '?'))
                    else:
                        decompounded = self.tool.splitTagByCompound(tag)
                        for analysis in decompounded:
                            _t = self.tool.splitAnalysis(analysis)
                            lemma = _t[0]
                            _tag = self.cleanTag(_t[1::])
                            _new = (_input, lemma, _tag)
                            if _new not in cleaned:
                                cleaned.append(_new)
        else:
            for _input, tags in lookups:
                for tag in tags:
                    # TODO: how does OBT handle unknown?
                    if '+?' in tag:
                        unknown = True
                        cleaned.append((_input, '?', '?'))
                    else:
                        tag = self.tool.splitAnalysis(tag)
                        lemma = tag[0]
                        _tag = self.cleanTag(tag[1::])
                        cleaned.append((_input, lemma, _tag))

        return cleaned

    def __init__(self, languagecode, tagsets={}):
        self.langcode = languagecode

        import logging
        logfile = logging.FileHandler('morph_log.txt')
        FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        self.logger = logging.Logger('morphology', level=0)
        self.logger.setLevel(logging.ERROR)
        self.logger.addHandler(logfile)

        self.tagsets = Tagsets(tagsets)

def sme_test():
    sme_options = {
        'compoundBoundary': "  + #",
        'derivationMarker': "suff.",
        'tagsep': ' ',
        'inverse_tagsep': '+',
    }

    smexfst = XFST(lookup_tool='/Users/pyry/bin/lookup',
                   fst_file='/Users/pyry/gtsvn/gt/sme/bin/n-sme.fst',
                   ifst_file='/Users/pyry/gtsvn/gt/sme/bin/isme.fst',
                   options=sme_options)

    sme = smexfst >> Morphology('sme')

    return sme

def sme_derivation_test():
    sme = sme_test()

    test_words = [
        u'borahuvvat',
        u'juhkaluvvan'
    ]
    for w in test_words:
        print "No options"
        print sme.lemmatize(w)

        print "/lookup/ lemmatizer"
        print sme.lemmatize( w
                           , split_compounds=True
                           , non_compound_only=True
                           , no_derivations=True
                           )
        
        print "/ search analyzer"
        print sme.analyze( w
                         , split_compounds=True
                         )

def sme_compound_test():
    # TODO: make UnitTests out of these.
    sme = sme_test()

    print "No options"
    print sme.lemmatize(u'báhčinsearvi')

    print "Strip derivation, compounds, but also split compounds"
    print sme.lemmatize( u'báhčinsearvi'
                       , split_compounds=True
                       , non_compound_only=True
                       , no_derivations=True
                       )

    print "Strip derivation, but also split compounds"
    print sme.lemmatize( u'báhčinsearvi'
                       , split_compounds=True
                       , no_derivations=True
                       )

    print "Strip compounds, but also split compounds"
    print sme.lemmatize( u'báhčinsearvi'
                       , split_compounds=True
                       , non_compound_only=True
                       )

    print "Strip compounds"
    print sme.lemmatize( u'báhčinsearvi'
                       , non_compound_only=True
                       )

    print "Split compounds"
    print sme.lemmatize( u'báhčinsearvi'
                       , split_compounds=True
                       )
    
    print sme.lemmatize( u'boazodoallošiehtadallanlávdegotti'
                       , split_compounds=True
                       , non_compound_only=True
                       , no_derivations=True
                       )

def examples():
    # TODO: make this into tests

    obt = OBT('/Users/pyry/gtsvn/st/nob/obt/bin/mtag-osx64')

    nob = obt >> Morphology('nob')
    print
    print ' -- nob --'
    print ' ingen: '
    for a in nob.lemmatize(u'ingen'):
        print '  ' + a

    print ' tålt: '
    for a in nob.lemmatize(u'tålt'):
        print '  ' + a

    sme = sme_test()
    print
    print ' -- sme lemmatize --'
    print ' mánnat: '
    for a in sme.lemmatize(u'mannat'):
        print '  ' + a

    generate = sme.generate(u'mannat', [['V', 'Inf'],
                                ['V', 'Ind', 'Prs', 'Sg1'],
                                ['V', 'Ind', 'Pst', 'Sg2'],
                                ['V', 'Ind', 'Prt', 'Sg2']]
                                )
    
    for lem, tag, forms in generate:
        if forms:
            for form in forms:
                print '  ' + ' '.join(tag) + ' => ' + form
        else:
            print '  ' + ' '.join(tag) + ':   unknown'

    generate = sme.generate(u'eaktodáhtolašš', [['A', 'Attr'], ])
    
    for lem, tag, forms in generate:
        if forms:
            for form in forms:
                print '  ' + ' '.join(tag) + ' => ' + form
        else:
            print '  ' + ' '.join(tag) + ':   unknown'


    for a in sme.analyze(u'gullot'):
        print '  %s %s  %s' % (a[0], a[1], ' '.join(a[2]))

    print ' -- analyze with compounds -- '
    for a in sme.analyze(u'juovlaspábbačiekčangilvu', split_compounds=True):
        print '  %s %s  %s' % (a[0], a[1], ' '.join(a[2]))

    print ' -- analyze -- '
    for a in sme.analyze(u'juovlaspábbačiekčangilvu'):
        print '  %s %s  %s' % (a[0], a[1], ' '.join(a[2]))

    print ' -- lemmatize -- '
    for a in sme.lemmatize(u'spábbačiekčangilvu'):
        print '  ' + a

    print ' -- lemmatize with compounds -- '
    for a in sme.lemmatize(u'juovlaspábbačiekčangilvu', split_compounds=True):
        print '  ' + a

    print ' -- lemmatize -- '
    for a in sme.lemmatize(u'juovlaspábbačiekčangilvu'):
        print '  ' + a

def tag_examples():
    setdefs = {
        'type': ["NomAg", "G3"],
        'person': ["Sg1", "Sg2", "Sg3"],
    }

    tagsets = Tagsets(setdefs)
    tag_test = Tag('N+NomAg+Sg+Ill', sep='+')
    print tag_test

    _type = tagsets['type']
    for m in _type.members:
        print m

    print tag_test.getTagByTagset(_type)
    print tag_test[_type]

    for item in tag_test:
        print item

if __name__ == "__main__":
    # examples()
    # tag_examples()
    # sme_compound_test()
    sme_derivation_test()

