#!/usr/bin/env python2

import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import number

flags = []
key_path = flag_path = ''

def load_flags():
    global flags
    try:
        with open(flag_path, "rb") as f:
            flags = [line.strip() for line in f.readlines()]
    except:
        print("Failed to load the flags")
        quit()

def load_key():
    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except:
        print("Failed to open the key")
        quit()

    return key

def read_file(filename):
    try:
        with open(filename, "rb") as f:
            data = f.read()
    except:
        print("File not found!")
        quit()

    return data

def load_config():
    global key_path, flag_path
    try:
        with open("config", "rb") as f:
            path = f.readline().strip()
            key_path = "%s/key" % path
            flag_path = "%s/flags" % path
    except:
        print("failed to load the config")
        quit()


def game():
    # generate p/q
    g = number.getPrime(20)
    p = number.getPrime(20)

    # get a random prime number as a quiz
    random_b = number.getPrime(10)
    # calculate (g**b) % p, i.e., g^b mod p
    gb_p = pow(g, random_b, p)

    print("Public keys: g = %d, p = %d" % (g, p))
    print("My number is: %d" % gb_p)
    print("Give me your number:")
    your_number = int(raw_input())
    if (your_number == 0 or your_number == 1):
        print("Don't send 0 or 1")
        quit()

    shared_secret = pow(your_number, random_b, p)

    print("Give me your shared secret:")
    your_shared_secret = int(raw_input())

    if your_shared_secret != shared_secret:
        print("Incorrect: You sent me %d but my one was %d" %
                (your_shared_secret, shared_secret))
        quit()
    else:
        print("Correct! My b was %d and pow(%d, %d, %d) = %d.\nUse this as the key for the block cipher!" % (random_b, your_number, random_b, p, shared_secret))



# TODO: read this function first
def main():
    # load the flag securely
    load_flags()

    print("RAW Diffie--Hellman")
    print("Please win 10 games")

    for i in range(10):
        game()

    print(flags)

if __name__ == '__main__':
    load_config()
    main()
