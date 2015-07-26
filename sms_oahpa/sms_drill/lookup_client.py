#!/usr/bin/env python

"""
A lookupserv client for testing. This is the simplest possible example,
and uses python's default telnetlib
"""

from .models import Tag

def init_logger():

    import logging
    from logging.handlers import WatchedFileHandler
    FORMAT = '%(message)s'
    formatter = logging.Formatter(fmt=FORMAT)

    handler = WatchedFileHandler('sms_lookup_client.log', mode='a')
    handler.setFormatter(formatter)


    client_log = logging.getLogger('lookup_client')
    client_log.setLevel(logging.INFO)
    client_log.addHandler(handler)

    return client_log


client_log = init_logger()

def log(*args):

    a_str = ''
    if len(args) > 0:
        for a in args:
            try:
                a_str += ' ' + a
            except:
                a_str += ' ' +repr(a)

    try:
        s = a_str.encode('utf-8')
    except:
        s = a_str
    client_log.info(s)


def send_lookup(tool_name, input_string, host='127.0.0.1', port=9001, timeout=2, until='\n\n'):
    import telnetlib
    import sys

    if len(input_string) == 0:
        return False, ''

    try:
        data_to_send = input_string.encode('utf-8')
    except:
        data_to_send = input_string

    # connect
    t = telnetlib.Telnet()
    t.open(host, port, timeout)

    # send the command
    t.write("%s\n%s\n" % (tool_name, input_string))

    d = t.read_until(until, 2).decode('utf-8')
    t.close()

    if 'ERROR' in d:
        return False, d
    
    return True, d

def lookup(*args, **kwargs):
    """
        Clean XFST lookup text, perform lookups in the database for
        corresponding lemmas and tags.

        Returns (success, lookup_list):
            success - boolean
            lookup_list - any lookups present

        Success is false if there were no lookups.

    """

    from .models import Tag, Word

    success, lookup_string = send_lookup(*args, **kwargs)

    def clean_analysis(analysis):
        """ Convert analyses to db objects.

            TODO: if lemma exists, but isn't in db, what then? We don't
            care about these lemmas, probably, because we only care
            about the one the DB generated

        """
        lemma, _, tag = analysis.partition('+')
        log(lemma)

        if analysis.endswith('+?'):
            return (False, False)

        try:
            l = Word.objects.get(lemma=lemma)
        except Word.DoesNotExist:
            return (False, False)

        t, created = Tag.objects.get_or_create(string=tag)

        if created:
            log('>> lookup tool returned tag not in DB, created: ' + repr(t))
        return (l, t)

    def split_a_line(analysis_line):
        wf, _, tag = analysis_line.partition('\t')

        l, t_obj = clean_analysis(tag)
        if l and t_obj:
            return (l, t_obj)
        else:
            return (False, False)

    analysis_chunks = [a for a in lookup_string.split('\n\n') if a.strip()]

    cleaned = []
    for chunk in analysis_chunks:
        lemmas = []
        analyses = []

        for part in chunk.split('\n'):
            (lemma, analysis) = split_a_line(part)
            lemmas.append(lemma)
            analyses.append(analysis)

        lemma = list(set(lemmas))[0]

        append_ = (lemma, analyses)

        cleaned.append(append_)

    # TODO: filter out null analyses in cleaned, if none exist, then
    # success = False

    log("--")
    log("success    ", success)
    log("analysis    ", cleaned)

    if success:
        return success, cleaned
    else:
        return False, []
