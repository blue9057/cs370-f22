#!/usr/bin/env python3

import socket

def main():
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 31337))

    print("Sending Hello...")
    client_socket.send(b'Hello\n')

    b_number = client_socket.recv(5)
    s_number = str(b_number, 'utf-8')
    print("Received %s" % s_number.strip())

    i_number = int(s_number)
    i_answer = i_number + 1

    print("Returning %d" % i_answer)
    b_answer = bytes(str(i_answer), 'utf-8')
    client_socket.send(b_answer)

    result = client_socket.recv(10)
    print(result)

    client_socket.close()

if __name__ == '__main__':
    main()
