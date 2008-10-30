# -*- coding: utf-8 -*-
#
# TCP-client for testing the lookup server.
#
# usage: client.py
#

import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8090))
while 1:
    data = raw_input ( "SEND( TYPE q or Q to Quit):" )
    if (data <> 'Q' and data <> 'q'):
        client_socket.send(data)
    else:
        client_socket.send(data)
        client_socket.close()
        break

    data = client_socket.recv(512)
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break
    else:
        print data
