#!/usr/bin/env python

"""
A lookupserv client for testing. This is the simplest possible example,
and uses python's default telnetlib
"""

def lookup(tool_name, input_string, host='127.0.0.1', port=9001, timeout=2, until='\n\n'):
    """
        >>> lookup('cat', 'bbq', port=9009)
        (True, 'bbq')
        >>> lookup('cats', 'bbqs', port=9009)
        (True, 'bbqs')
        >>> lookup('nocats', 'bbqs', port=9009)
        (False, 'ERROR: nonexistent utility')
    """

    import telnetlib
    import sys

    try:
        data_to_send = input_string.encode('utf-8')
    except:
        data_to_send = input_string

    # connect
    t = telnetlib.Telnet()
    t.open(host, port, timeout)

    # send the command
    t.write("%s\n%s\n" % (tool_name, input_string))

    d = t.read_until(until, 2)
    t.close()

    if 'ERROR' in d:
        return False, d
    
    return True, d
