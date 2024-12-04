#!/usr/bin/env python2

import random

from pwn import *

def lprint(msg):
    print(msg.ljust(80))

def rprint(msg):
    print(msg.rjust(80))

def solve_game(p):
    ##########################################################################
    # DO NOT EDIT                                                            #
    ##########################################################################
    str_public_keys = p.readline().strip()
    lprint(str_public_keys)
    pks = str_public_keys.split(':')[1].strip().split(',')
    g, P = [int(s.split('=')[1].strip()) for s in pks]
    lprint("Received g %d p %d" % (g, P))

    # get the exchange message, i.e., g ** b % P
    exchange_msg = p.readline().strip()
    exchange_number = int(exchange_msg.split(':')[1].strip())
    lprint('Exchanged number: %d (g ** b mod P)' % exchange_number)
    ##########################################################################

    # TODO: We will choose a random number, a, and share g ** a % P,
    #       i.e., pow(g, a, P) to the other side.
    #       Note that we will never share 'a' directly.

    # choose a
    p.readline().strip()
    a = random.randint(1000,5000)
    rprint("My secret a (never sent to the program) is: %d" % a)

    # TODO: your code...
    result = pow(1, 1, 1)
    p.sendline(str(result))
    rprint("g ** a mod P is: %d" % result)

    # give me your shared secret
    print(p.readline().strip())

    # TODO: your code here...
    shared_secret = pow(1, 1, 1)
    p.sendline(str(shared_secret))
    rprint("Sending (g**b)**a mod P: %d" % shared_secret)

    print(p.readline().strip())
    print(p.readline().strip())


# TODO: the program starts at here..
def main():
    p = process("./dh.py")

    # read intro messages
    print(p.readline().strip())
    print(p.readline().strip())

    # run 10 games
    for i in range(10):
        solve_game(p)
        raw_input("Press ENTER to continue...\n\n")

    # will get the flag after the game finishes
    p.interactive()


if __name__ == '__main__':
    main()
