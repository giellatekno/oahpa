import sys

import circuits
from circuits import Component, Debugger, handler
from circuits.net.sockets import TCPServer
from circuits.net.events import write

import threading

# https://bitbucket.org/circuits/circuits/src/4e32ca556c376f981371aeffed2f087538e4138c/examples/chatserver.py?at=default

class Telnet(Component):

    channel = "server"

    def init(self, *args, **kwargs):
        """Initialize our ``ChatServer`` Component.

        This uses the convenience ``init`` method which is called after the
        component is properly constructed and initialized and passed the
        same args and kwargs that were passed during construction.
        """

        self.args = args
        self.opts = kwargs
        self.utilities = self.opts.pop('utilities')

        self.clients = {}

        if self.opts['debug']:
            Debugger().register(self)

        address, port = self.opts['bind']
        port = int(port)

        bind = (address, port)

        TCPServer(bind).register(self)

    def broadcast(self, data, exclude=None):
        exclude = exclude or []
        targets = (sock for sock in self.clients.keys() if sock not in exclude)
        for target in targets:
            self.fire(write(target, data))

    def connect(self, sock, host, port):
        """Connect Event -- Triggered for new connecting clients"""

        self.clients[sock] = {
            "host": sock,
            "port": port,
            "state": {
                "utility": None,
                "registered": False
            }
        }

        self.fire(write(sock, b"choose a util: "))

    def disconnect(self, sock):
        """Disconnect Event -- Triggered for disconnecting clients"""

        if sock not in self.clients:
            return

        utility = self.clients[sock]["state"]["utility"]

        del self.clients[sock]

    def read(self, sock, data):
        """Read Event -- Triggered for when client connections have data"""

        data = data.strip().decode("utf-8")

        if not self.clients[sock]["state"]["registered"]:
            utility = data

            self.clients[sock]["state"]["registered"] = True
            self.clients[sock]["state"]["utility"] = utility

        else:
            utility = self.clients[sock]["state"]["utility"]

        # Client sends null data, so we close the socket and disconnect
        # them.
        if not data.strip():
            self.disconnect(sock)
            sock.close()
            return

        # Otherwise send data off for lookup
        # 
        print repr(self.clients[sock]["state"]["utility"])
        print repr(data)

class TelnetListener(threading.Thread):

    def __init__(self, server_options, utilities):
        self.options = server_options
        self.utilities = utilities

        self.host = "127.0.0.1"
        self.port = self.options.get('port')

        threading.Thread.__init__(self)

        # threading: Die when app dies.
        self.setDaemon(True)

    def run(self):
        # do whatever to run server and handle clients
        from circuits import Debugger

        print 'preparing telnet host on <%s:%d>' % (self.host, self.port)
        self.t = Telnet(bind=(self.host, self.port),
                        utilities=self.utilities, debug=True)
        self.t.run()

        # listen for work, and perform work
        while True:
            time.sleep(0.1)

