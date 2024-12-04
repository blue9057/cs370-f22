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

def usage():
        print("Please generate the RSA key by copying the template.py file" + \
                " as a solution.py, write your code, and then, run it before" + \
                "running ./launcher")
        quit()


def game():
    # generate p/q
    p = number.getPrime(10)
    q = number.getPrime(10)
    # calculate N and phi
    N = p*q
    phi = (p-1) * (q-1)
    # set e as a prime under 10 bits < 2 ** 10
    e = 337
    # find d - brute forcing (SLOW but works)
    d = 0
    for i in range(1048576):
        if (e*i % phi) == 1:
            d = i

    # get a random prime number as a quiz
    random_prime = number.getPrime(8)
    print("Public keys: N = %d, e = %d" % (N, e))
    print("Please encrypt the following number and send back to me: %d" % random_prime)
    ciphertext = int(raw_input())
    decrypted = pow(ciphertext, d, N)

    if decrypted != random_prime:
        print("Incorrect: You sent me %d but the correct one was %d" %
                (decrypted, random_prime))
        quit()
    else:
        print("Correct!, my number was %d and its encryption was %d" % (random_prime, ciphertext))

    # get a random prime number as a quiz 2
    random_prime = number.getPrime(8)
    ciphertext = pow(random_prime, e, N)
    print("Private key: D = %d" % (d))
    print("What is the decryption of ciphertext: %d" % ciphertext)
    decrypted = int(raw_input())

    if decrypted != random_prime:
        print("Incorrect: You sent me %d but the correct one was %d" %
                (decrypted, random_prime))
        quit()
    else:
        print("Correct!, my number was %d" % random_prime)



# TODO: read this function first
def main():
    # load the flag securely
    load_flags()

    print("RAW RSA")
    print("Please win 10 games")

    for i in range(10):
        game()

    print(flags)

if __name__ == '__main__':
    load_config()
    main()
