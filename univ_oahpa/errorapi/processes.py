from .log import ERROR_FST_LOG

class XFST(object):

    def clean(self, _output):
        """
            Clean XFST lookup text into

            [('keenaa', ['keen+V+1Sg+Ind+Pres', 'keen+V+3SgM+Ind+Pres']),
             ('keentaa', ['keen+V+2Sg+Ind+Pres', 'keen+V+3SgF+Ind+Pres'])]

        """

        analysis_chunks = [a for a in _output.split('\n\n') if a.strip()]

        def split_tag(t):
            return t.split('+')

        def split_analysis(a):
            lem, _, tag = a.partition('+')
            return (lem, split_tag(tag))

        cleaned = []
        for chunk in analysis_chunks:
            lemmas = []
            analyses = []

            for part in chunk.split('\n'):
                wordform, _, analysis = part.partition('\t')
                lemmas.append(wordform)
                analyses.append(split_analysis(analysis))
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

        try:
            _input = _input.encode('utf-8')
        except:
            pass

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
            try:
                output = output.decode('utf-8')
            except:
                pass

        if err:
            try:
                err = err.decode('utf-8')
            except:
                pass

        return (output, err)

    def __init__(self, lookup_tool, fst_file, **options):
        self.cmd = "%s %s" % (lookup_tool, fst_file)
        self.options = options

        if 'logger' in options:
            self.logger = options.get('logger')
        else:
            self.logger = ERROR_FST_LOG

    def lookup(self, lookups_list):
        lookup_string = '\n'.join(lookups_list)
        output, err = self._exec(lookup_string, cmd=self.cmd)
        if len(output) == 0 and len(err) > 0:
            name = self.__class__.__name__
            msg = """%s: %s""" % (name, err)
            self.logger.error(msg.strip())
        return self.clean(output)
