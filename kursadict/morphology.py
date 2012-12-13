#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Morphological tools
"""

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
        self.options = {'compoundBoundary': "+Cmp#"}

        if ifst_file:
            self.icmd = "%s -flags mbTT %s" % (lookup_tool, ifst_file)
        else:
            self.icmd = False

    def __rshift__(left, right):
        right.tool = left
        return right

    def lookup(self, lookups_list):
        lookup_string = '\n'.join(lookups_list)
        output, err = self._exec(lookup_string, cmd=self.cmd)
        return self.clean(output)

    def inverselookup(self, lemma, tags):

        if not self.icmd:
            print >> sys.stderr, " * Inverse lookups not available."
            return False

        lookups_list = []
        for tag in tags:
            lookups_list.append(self.formatTag([lemma] + tag))
        lookup_string = '\n'.join(lookups_list)
        output, err = self._exec(lookup_string, cmd=self.icmd)
        return self.clean(output)

    def tagUnknown(self, analysis):
        if '+?' in analysis:
            return True
        else:
            return False

    def formatTag(self, parts):
        return '+'.join(parts)

    def splitAnalysis(self, analysis):
        """ u'lemma+Tag+Tag+Tag' -> [u'lemma', u'Tag', u'Tag', u'Tag'] """
        return analysis.split('+')


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

            if not unknown:
                parts = self.tool.splitAnalysis(tag)
                lemma = parts[0]
                tag = self.cleanTag(parts[1::])
                reformatted.append((lemma, tag, forms))
            else:
                parts = self.tool.splitAnalysis(tag)
                lemma = parts[0]
                tag = parts[1::]
                forms = False
                reformatted.append((lemma, tag, forms))

        return reformatted


    def lemmatize(self, form, split_compounds=False):
        """ For a wordform, return a list of lemmas
        """
        lookups = self.tool.lookup([form])
        if split_compounds:
            lemmas = []
            for _form, analyses in lookups:
                decompounded = sum(map(self.tool.splitTagByCompound, analyses), [])
                for analysis in decompounded:
                    _lem = self.tool.splitAnalysis(analysis)[0]
                    if _lem not in lemmas:
                        lemmas.append(_lem)
        else:
            lemmas = set()
            for _form, analyses in lookups:
                for analysis in analyses:
                    lemmas.add(self.tool.splitAnalysis(analysis)[0])
            lemmas = list(lemmas)

        return lemmas

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

    def __init__(self, languagecode):
        self.langcode = languagecode


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

    smexfst = XFST(lookup_tool='/Users/pyry/bin/lookup',
                   fst_file='/Users/pyry/gtsvn/gt/sme/bin/sme.fst',
                   ifst_file='/Users/pyry/gtsvn/gt/sme/bin/isme.fst')

    sme = smexfst >> Morphology('sme')
    print
    print ' -- sme --'
    print ' mánnat: '
    for a in sme.lemmatize(u'mánnat'):
        print '  ' + a

    generate = sme.generate(u'mánnat', [['V', 'TV', 'Inf'],
                                ['V', 'TV', 'Ind', 'Prs', 'Sg1'],
                                ['V', 'TV', 'Ind', 'Pst', 'Sg2'],
                                ['V', 'TV', 'Ind', 'Prt', 'Sg2']]
                                )
    for lem, tag, forms in generate:
        if forms:
            for form in forms:
                print '  ' + ' '.join(tag) + ' => ' + form
        else:
            print '  ' + ' '.join(tag) + ':   unknown'

    for a in sme.analyze(u'gullot'):
        print '  %s	%s	%s' % (a[0], a[1], '+'.join(a[2]))

    print ' -- analyze with compounds -- '
    for a in sme.analyze(u'juovlaspábbačiekčangilvu', split_compounds=True):
        print '  %s	%s	%s' % (a[0], a[1], '+'.join(a[2]))

    print ' -- analyze -- '
    for a in sme.analyze(u'juovlaspábbačiekčangilvu'):
        print '  %s	%s	%s' % (a[0], a[1], '+'.join(a[2]))

    print
    print ' -- sme --'
    print ' mánnat: '
    for a in sme.lemmatize(u'mánnat'):
        print '  ' + a

    print ' -- lemmatize -- '
    for a in sme.lemmatize(u'spábbačiekčangilvu'):
        print '  ' + a

    print ' -- lemmatize with compounds -- '
    for a in sme.lemmatize(u'juovlaspábbačiekčangilvu', split_compounds=True):
        print '  ' + a
    print ' -- lemmatize -- '
    for a in sme.lemmatize(u'juovlaspábbačiekčangilvu'):
        print '  ' + a

if __name__ == "__main__":
    examples()

