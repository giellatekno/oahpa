#!/usr/bin/env python

"""
A lookup server that uses threads to handle multiple clients at a time.
"""

import select
import pexpect
import socket
import sys
import re
import threading

class Server:
    def __init__(self):
        self.host = ''
        self.port = 9000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
                print "Could not open socket: " + message
                sys.exit(1)
                    
    def run(self):
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])
            
            for s in inputready:
                
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                    
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                    
                    # close all threads
                        
        self.server.close()
        for c in self.threads:
            c.join()
                            
class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

        fstdir="/opt/smi/sme/bin"
        lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup"
        lookup2cg = " | lookup2cg"
        preprocess = " | /usr/local/bin/preprocess "

        fst = fstdir + "/sme.fst"
        lookup = lo + " -flags mbTT -utf8 -d " + fst
        self.look = pexpect.spawn(lookup)
        
    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if not data or not data.strip():
                self.client.close()
                running = 0
            data2=data
            c = [";","<",">","*","|","`","&","$","!","#","(",")","[","]","{","}",":"]
            for a in c:
                data = data.replace(a,'')
            if not data:
                self.client.send(data2)
                continue
            self.look.sendline(data)
            self.look.expect ('\r?\n\r?\n')
            result = self.look.before
            print result
            # hack for removing the stderr from lookup 0%>>>>>>100% ...
            result = result.replace('100%','')
            result = result.replace('0%','')

            string =""
            for r in result.splitlines():
                res = r.rstrip('>').lstrip('>')
                if res.rstrip().lstrip():
                    string = string + res + "\n" 

            cg_call = "echo \"" + string + "\"" + lookup2cg
            anl = os.popen(cg_call).readlines()

            analyzed = ""
            for a in anl:
                analyzed = analyzed + a

            self.client.send(analyzed)

                    
if __name__ == "__main__":
    s = Server()
    s.run()
