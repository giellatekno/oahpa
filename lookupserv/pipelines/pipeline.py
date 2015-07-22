## 
# zmq queue -> Pipeline

# TODO: 
#   - here we need to figure out a way to hold the processes open and
#   read from them in a non-annoying way

import zmq
import sys, os

import threading
import subprocess

class Pipeline(threading.Thread):
    """ This is a string of one or more processes, where the stdout of
    the first is chained to the stdin of the next.
    """

    @property
    def subprocess(self):
        from subprocess import PIPE

        if self._subprocess is not None:
            return self._subprocess

        stdin = PIPE
        stdout = PIPE
        stderr = PIPE

        more = True

        try:
            self._subprocess = subprocess.Popen(self.cmd_string,
                                               shell=True,
                                               stdout=stdin,
                                               stdin=stdout,
                                               stderr=stderr,
                                               close_fds=True)
        except OSError:
            # TODO: handle better.
            print "Problem executing cmd string. Check yaml defs"
            print self.cmd_string

        return self._subprocess

    def __init__(self, context, process, options):
        self.cmd_string = process
        self._subprocess = None

        self.options = options
        self.context = context

        threading.Thread.__init__(self)

        # threading: Die when app dies.
        self.setDaemon(True)

    def run(self):
        self.subprocess
        self.listen_for_work()

    def log_work(self, result_str):
        log_file_path = os.path.join('logs/', "%s.result.log" % self.options.get('name'))

        with open(log_file_path, 'a') as F:
            F.write(result_str)

    def read(self, src=False):
        out, _ = self.subprocess.communicate()
        self._subprocess = None
        return out

    def do_work(self, data):
        self.subprocess.stdin.write(data)
        out = self.read().decode('utf-8')
        return out

    def listen_for_work(self):
        import time

        socket_type = 'REP'

        listen = "ipc://socket_tmp/lserv-" + self.options.get('name')
        print >> sys.stdout, " ... Opening <%s>:<%s>" % (listen, socket_type)
        socket = self.context.socket(zmq.REP)
        socket.bind(listen)

        # listen for work, and perform work
        while True:
            req = socket.recv()
            res = self.do_work(req)
            socket.send(res.encode('utf-8'))
            self.log_work(res.encode('utf-8'))
            time.sleep(0.002)


class PipelineQueue(object):

    def __init__(self, context, options):

        self.context = context
        self.connect = "ipc://socket_tmp/lserv-" + options.get('name')

        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.connect)

        self.pipeline = Pipeline(context, options.get('pipeline'), options)

        self.pipeline.start()

