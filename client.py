#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    METHOD = sys.argv[1]
    CLIENT_DATA = sys.argv[2]
    divide = CLIENT_DATA.split("@")[1].split(":")
    SERVER = divide[0]
    PORT = int(divide[1])
except IndexError:
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

LINE = ' sip:' + CLIENT_DATA + ' SIP/2.0\r\n'

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print("Enviando: " + METHOD + LINE)
    my_socket.send(bytes(METHOD + LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    response = data.decode('utf-8').split("\r\n")
    if(response[0].split()[1] == '100' and METHOD == 'INVITE'):
        my_socket.send(bytes('ACK' + LINE, 'utf-8') + b'\r\n')
    print('Recibido --', data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
