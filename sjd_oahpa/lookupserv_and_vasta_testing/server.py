# -*- coding: utf-8 -*-
#
# TCP-server for lookup. Called from the ped-interface (forms.py)
#
# usage: server.py
#

import socket
import pexpect
import os
import re

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 9000))
server_socket.listen(5)

fstdir="/opt/smi/sme/bin"
lo = "/usr/local/bin/lookup"
# lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup" # commercial
lookup2cg = " | lookup2cg"
cg3 = "vislcg3"
preprocess = " | /usr/local/bin/preprocess "
dis = "/opt/smi/sme/bin/sme-ped.cg3.bin"

#fstdir="/Users/saara/gt/sme/bin"
#lo = "/Users/saara/bin/lookup"
#lookup2cg = " | /Users/saara/gt/script/lookup2cg"
#cg3 = "/usr/local/bin/vislcg3"
#preprocess = " | /Users/saara/gt/script/preprocess "
#dis = "/Users/saara/ped/sme/src/sme-ped.cg3"

fst = fstdir + "/sme.fst"
#fst = fstdir + "/ped-sme.fst"
lookup = lo + " -flags mbTT -utf8 -d " + fst 
vislcg3 = cg3 + " --grammar " + dis + " -C UTF-8"
disamb = " | " + cg3 + " --grammar " + dis + " -C UTF-8"

look = pexpect.spawn(lookup)
disambiguate = pexpect.spawn(vislcg3)


print "TCPServer Waiting for client on port 9000"

while 1:
    client_socket, address = server_socket.accept()
    print "I got a connection from ", address
    while 1:            
        data = client_socket.recv(512)
        if ( data == 'q' or data == 'Q'):
            client_socket.close()
            break
        else:
            print "RECIEVED:" , data
            if not data:
                client_socket.close()
                break				
            if not data.lstrip().rstrip():
                client_socket.close()
                break
            data2=data
            c = [";","<",">","*","|","`","&","$","!","#","(",")","[","]","{","}",":"]
            for a in c:
                data = data.replace(a,'')
            if not data:
                client_socket.send(data2)
                continue
            look.sendline(data)
            look.expect ('\r?\n\r?\n')
            result = look.before

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

            client_socket.send(analyzed)
            
            #analyzed = analyzed + "jee\n"
            #print analyzed
            #print "*****"
            #disambiguate.send(analyzed)
            #disambiguate.expect ('jee')

            #print disambiguate.before
            #print "--------"
            #client_socket.send(disambiguate.before)
