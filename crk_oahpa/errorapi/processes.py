from .log import ERROR_FST_LOG
from django.conf import settings

ERROR_FST_SETTINGS = settings.ERROR_FST_SETTINGS

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

        print cmd
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

class FeedbackFST(object):

    def _error_tags_from_fst(self, fst_response):
        """ Grab the error tags returned in the FST response, based on
        the tags available in the message store.
        """

        from sets import ImmutableSet

        error_tags = []
        for wf, analyses in fst_response:
            for lem, tag in analyses:
                # TODO: tagsets instead?
                existing_errors = \
                    set(tag) & set(self.message_store.error_tags)
                if len(existing_errors) > 0:
                    error_tags.append(ImmutableSet(existing_errors))

        error_tags = list(set(error_tags))

        return error_tags

    def _messages_for_error_tags(self, error_tags, display_lang, task=False, wordform='WORDFORM'):
        error_messages = []

        def replace_string(msg):
            if 'title' in msg:
                msg["title"] = msg["title"].replace('WORDFORM', '"%s"' % wordform)
            msg["description"] = msg["description"].replace('WORDFORM', '"%s"' % wordform)
            return msg

        # TODO: is this an issue? 
        #  For this part need to get a message with the maximal match,
        # so:
        #   ['Acc', 'CGErr', 'Gen']
        #  can match ['Acc', 'CGErr']

        for err_tag in error_tags:
            if task:
                message = self.message_store.get_message(display_lang, err_tag, task=task)
            else:
                message = self.message_store.get_message(display_lang, err_tag)
            if message:
                error_messages.append({
                    'tags': err_tag,
                    'message': map(replace_string, message)
                })

        return error_messages

    def get_all_feedback_for_form(self, input_wordform, task=False,
                                  intended_lemma=False, display_lang='nob'):
        """ Accepts a wordform, returns feedback error tags and
        messages.
        """
        # TODO: cache input-output for some period of time, or until
        # last update + created date of FST file is changed? 

        fst_response = self.lookup_proc.lookup([input_wordform])

        if intended_lemma:

            def lemma_filter(o):
                result = []
                for (wf, analyses) in o:
                    filtered = []
                    for lem, tag in analyses:
                        if unicode(lem) == unicode(intended_lemma):
                            filtered.append((lem, tag))
                    result.append((wf, filtered))
                return result

            fst_response = lemma_filter(fst_response)

        error_tags = self._error_tags_from_fst(fst_response)

        error_messages = self._messages_for_error_tags(error_tags, display_lang, task=task, wordform=input_wordform)

        return {
            'fst': fst_response,
            'error_tags': error_tags,
            'messages': error_messages
        }

    def __init__(self, message_store):

        self.lookup_proc = XFST(
            ERROR_FST_SETTINGS.get('lookup_tool'),
            ERROR_FST_SETTINGS.get('fst_path'),
        )
        self.message_store = message_store
