#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

try:
    PORT = int(sys.argv[2])
    AUDIO = sys.argv[3]
except IndexError:
    sys.exit("Usage: python3 server.py IP port audio_file")

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        IP = self.client_address[0]
        PORT = str(self.client_address[1])
        MP32RTP = './mp32rtp -i 127.0.0.1 -p 23032 <' + AUDIO
        print("IPCliente: " + IP + " PuertoCliente: " + PORT)
        while 1:
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))
            if not line or '\n':
                break
        method = str.upper(line.decode('utf-8').split(" ")[0])
        if method == 'INVITE':
            self.wfile.write(b'SIP/2.0 100 Trying\r\n\r\n')
            self.wfile.write(b'SIP/2.0 180 Ring\r\n\r\n')
            self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
        elif method == 'ACK':
            os.system(MP32RTP)
        elif method == 'BYE':
            self.wfile.write(b'SIP/2.0 200 OK \r\n\r\n')
        else:
            self.wfile.write(b'SIP/2.0 405 Method not Allowed\r\n\r\n')

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit('Finalizado Servidor')
