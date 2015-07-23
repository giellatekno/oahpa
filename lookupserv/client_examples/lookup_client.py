#!/usr/bin/env python

"""
A lookupserv client for command line testing.
Entering a blank line will exit the client.
"""

def lookup(tool_name, input_string, host='127.0.0.1', port=9001, timeout=2, until='\n\n'):
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

def main():
    print lookup("sme-cg", "son manai dohko.")
    print lookup("sme-analyze", "manai")

    # This is purposefully an error
    print lookup("sme-analyzer", "manai")

if __name__ == "__main__":
    import sys
    sys.exit(main())
