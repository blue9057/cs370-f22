#!/usr/bin/env python3

import socket
import ssl

def main():
    client_socket = socket.socket()

    context = ssl.create_default_context()
    context.check_hostname = False          # bad example
    context.verify_mode = ssl.CERT_NONE     # bad example

    client_socket.connect(('127.0.0.1', 31337))
    ssl_client_socket = context.wrap_socket(client_socket)

    print("Sending Hello...")
    ssl_client_socket.send(b'Hello\n')

    b_number = ssl_client_socket.recv(5)
    s_number = str(b_number, 'utf-8')
    print("Received %s" % s_number.strip())

    i_number = int(s_number)
    i_answer = i_number + 1

    print("Returning %d" % i_answer)
    b_answer = bytes(str(i_answer), 'utf-8')
    ssl_client_socket.send(b_answer)

    result = ssl_client_socket.recv(10)
    print(result)

    ssl_client_socket.close()

if __name__ == '__main__':
    main()
