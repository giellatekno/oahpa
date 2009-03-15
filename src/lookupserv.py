#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A lookup server that uses threads to handle multiple clients at a time.
Called from the ped-interface (forms.py)
"""

import select
import pexpect
import socket
import sys
import re
import os
import threading
import time

class Server:
    def __init__(self):
        self.host = ''
        self.port = 9000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

        fstdir="/opt/smi/sme/bin"
        lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup"
        preprocess = " | /usr/local/bin/preprocess "

        fst = fstdir + "/ped-sme.fst"
        lookup = lo + " -flags mbTT -utf8 -d " + fst
        self.look = pexpect.spawn(lookup)
        
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
                    c = Client(self.server.accept(),self.look)
                    c.start()
                    self.threads.append(c)
            time.sleep(1)
                        
        self.server.close()
        for c in self.threads:
            c.join()
                            
class Client(threading.Thread):
    def __init__(self,(client,address),look):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.look=look
        self.lookup2cg = " | /usr/local/bin/lookup2cg"

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if not data or not data.strip():
                self.client.close()
                running = 0
                continue
			
            data2=data
			# clean the data for command line
            c = [";","<",">","*","|","`","&","$","!","#","(",")","[","]","{","}",":"]
            for a in c:
                data = data.replace(a,'')
			# if the data contained only special characters, return the original data.
            if not data:
                self.client.send(data2)
                continue
			# quit with q
            #print data
            if ( data.strip() == 'q' or data == 'Q'):
                self.client.close()
                running = 0				
                continue			
            self.look.sendline(data)
            self.look.expect('\r?\n\r?\n')
            result = self.look.before
            #print result
            # hack for removing the stderr from lookup 0%>>>>>>100% ...
            result = result.replace('100%','')
            result = result.replace('0%','')

            string =""
            for r in result.splitlines():
                res = r.rstrip('>').lstrip('>')
                if res.rstrip().lstrip():
                    string = string + res + "\n" 

            cg_call = "echo \"" + string + "\"" + self.lookup2cg
            anl = os.popen(cg_call).readlines()

            analyzed = ""
            for a in anl:
                analyzed = analyzed + a

            self.client.send(analyzed)

                    
if __name__ == "__main__":
    s = Server()
    s.run()
