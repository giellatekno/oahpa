#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Morphological tools
"""

# TODO: from yaml FSTs = settings.FSTs

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

    return cleanLookupsXFST(output)


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

def generateFromList(language_iso, lookup_strings):
    fstfile = FSTs.get(language_iso + '_gen', False)
    lookup_strings = map(encodeOrFail, lookup_strings)
    if not fstfile:
        print "No FST for language."
        return False

    results = lookupInFST(lookup_strings, fstfile, decodeOutput=True)

    return results

def cleanLookupsXFST(lookup_string):
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

class XFST(object):

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

    def __init__(self, lookup_tool, fst_file, ifst_file=False):
        self.cmd = "%s -flags mbTT %s" % (lookup_tool, fst_file)

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

    def formatTag(self, parts):
        return '+'.join(parts)

    def splitAnalysis(self, analysis):
        """ u'lemma+Tag+Tag+Tag' -> [u'lemma', u'Tag', u'Tag', u'Tag'] """
        return analysis.split('+')


class OBT(XFST):
	""" TODO: this is almost like CG, so separate out those things if necessary.
	"""
    def clean(self, _output):
        """
            Clean CG lookup text into

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

    def __init__(self, lookup_tool):
        self.cmd = lookup_tool


class Morphology(object):

    def generate(self, lemma, tagsets):
        """ Run the lookup command, parse output into
            [(lemma, ['Verb', 'Inf'], ['form1', 'form2'])]
        """
        res = self.tool.inverselookup(lemma, tagsets)
        reformatted = []
        for tag, forms in res:
            unknown = False
            for f in forms:
                if '+?' in f:
                    unknown = True

            if not unknown:
                parts = self.tool.splitAnalysis(tag)
                lemma = parts[0]
                tag = parts[1::]
                reformatted.append((lemma, tag, forms))
            else:
                parts = self.tool.splitAnalysis(tag)
                lemma = parts[0]
                tag = parts[1::]
                forms = False
                reformatted.append((lemma, tag, forms))

        return reformatted


    def lemmatize(self, form):
        """ For a wordform, return a list of lemmas
        """
        lookups = self.tool.lookup([form])
        lemmas = set()
        for _form, analyses in lookups:
            for analysis in analyses:
                lemmas.add(self.tool.splitAnalysis(analysis)[0])

        return list(lemmas)

    def __init__(self, languagecode):
        self.langcode = languagecode


def examples():
    xfst = XFST(lookup_tool='/Users/pyry/bin/lookup',
                fst_file='/Users/pyry/somorph-priv.git/bin/som.fst',
                ifst_file='/Users/pyry/somorph-priv.git/bin/isom.fst')

    som = xfst >> Morphology('som')

    print ' -- som --'
    print ' wanaagsan: '
    for a in som.lemmatize('wanaagsan'):
        print '  ' + a

    print ' keen'
    generate = som.generate('keen', [['V', 'Inf'],
                                ['V', '1Sg', 'Ind', 'Past'],
                                ['V', '2Sg', 'Ind', 'Past']])
    for lem, tag, forms in generate:
        for form in forms:
            print '  ' + ' '.join(tag) + ' => ' + form

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

if __name__ == "__main__":
    examples()

