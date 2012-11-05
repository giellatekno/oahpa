#!/usr/bin/env python2.7

from flup.server.fcgi import WSGIServer
from kursadict import app

if __name__ == '__main__':
    host = 'localhost'
    port = 2323
    addr = (host, port)
    app.debug = True
    WSGIServer(app, bindAddress=addr).run()
 
# vim: set ts=4 sw=4 tw=0 syntax=python expandtab:
