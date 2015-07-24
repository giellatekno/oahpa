#!/usr/bin/env python

"""
A lookupserv client for testing. This is the simplest possible example,
and uses python's default telnetlib
"""

from .models import Tag

def lookup(tool_name, input_string, host='127.0.0.1', port=9001, timeout=2, until='\n\n'):
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

def parse_lookup(lookup_string):
    """
        Clean XFST lookup text into

        [('keenaa', ['keen+V+1Sg+Ind+Pres', 'keen+V+3SgM+Ind+Pres']),
         ('keentaa', ['keen+V+2Sg+Ind+Pres', 'keen+V+3SgF+Ind+Pres'])]


        Borrowed from NDS

    """

    def clean_analysis(analysis):
        lemma, _, tag = analysis.partition('+')
        try:
            t = Tag.objects.get(string=tag)
        except Tag.DoesNotExist:
            print 'no <Tag> for: ' + tag
            return False, False
        return (lemma, t)

    def split_a_line(analysis_line):
        wf, _, tag = analysis_line.partition('\t')
        l, t_obj = clean_analysis(tag)
        if l:
            return (l, t_obj)
        else:
            return (wf, tag)

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

    return cleaned
