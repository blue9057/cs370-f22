#!/usr/bin/env python3

import os
import random
import socket
import ssl
import sys

def main():
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', 31337))
    server_socket.listen(10)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    ssl_server_socket = context.wrap_socket(server_socket, server_side=True)

    while True:
        conn, addr = ssl_server_socket.accept()
        if os.fork():
            conn.close()
        else:
            message = conn.recv(6)
            if (message != b'Hello\n'):
                sys.exit(-1)
            print(b"Received %s" % message)
            number = random.randint(1000,9999)
            print("Sending %d" % number)
            conn.send(bytes(str(number)+'\n', 'utf-8'))
            message = conn.recv(5)
            print(b"Received %s" % message)
            if number+1 != int(str(message, 'utf-8')):
                conn.send(b"Incorrect\n")
                print("Incorrect")
            else:
                conn.send(b"  Correct\n")
                print("Correct")
            conn.close()
            sys.exit(0)


if __name__ == '__main__':
    main()
