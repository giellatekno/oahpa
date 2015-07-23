import sys

import circuits
from circuits import Component, Debugger, handler
from circuits.net.sockets import TCPServer
from circuits.net.events import write

import threading

# TODO: error log file

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

        self.fire(write(sock, b""))

    def disconnect(self, sock):
        """Disconnect Event -- Triggered for disconnecting clients"""

        if sock not in self.clients:
            return

        utility = self.clients[sock]["state"]["utility"]

        del self.clients[sock]

    def read(self, sock, data):
        """Read Event -- Triggered for when client connections have data"""

        print repr(data)
        try:
            data = data.strip().decode("utf-8")
        except UnicodeDecodeError:
            data = ""
            return

        data_included = False

        if not self.clients[sock]["state"]["registered"]:
            d = data.replace('\n','')
            utility = d

            # maybe user included data already
            if utility not in self.utilities:
                utility, _, data = data.partition('\n')
                if utility in self.utilities:
                    data_included = True

            if utility not in self.utilities:
                return "ERROR: nonexistent utility"

            self.clients[sock]["state"]["registered"] = True
            self.clients[sock]["state"]["utility"] = utility

            if not data_included:
                return ""

        else:
            utility = self.clients[sock]["state"]["utility"]

        # Client sends null data, so we close the socket and disconnect
        # them.
        if not data_included:
            if not data.strip():
                self.disconnect(sock)
                sock.close()
                return

        # Otherwise send data off for lookup
        # 
        utility = self.clients[sock]["state"]["utility"]
        if not utility:
            return ""

        u = self.utilities.get(utility, False)
        if not u:
            return "ERROR: nonexistent utility"

        utility_queue = u.get('queue')
        utility_socket = utility_queue.socket

        utility_socket.send(data.encode('utf-8'))
        message = utility_socket.recv()

        return message


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
            time.sleep(0.02)

