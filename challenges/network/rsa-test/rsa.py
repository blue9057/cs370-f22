#!/usr/bin/env python2

import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

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


# TODO: read this function first
def main():
    # load the flag securely
    load_flags()

    print("RSA TEST VERIFIER")

    # path check for the public key
    if not os.path.exists("my_public_key.pem"):
        usage()
    # import an rsa public key
    with open("my_public_key.pem", "rb") as f:
        public_key_data = f.read()
    public_key = RSA.import_key(public_key_data)

    print("Public key was loaded successfully: ")
    print(public_key_data)

    # create a PKCS1_OAEP cipher for
    # public key : encryption and verify
    cipher_rsa_public = PKCS1_OAEP.new(public_key)

    # our signature string
    string = 'CS370 Introduction to Security'

    # read your signature
    if not os.path.exists("signature"):
        usage()

    with open("signature", "rb") as f:
        signature = f.read()

    # verify your signature
    verification = cipher_rsa_public.encrypt(signature)
    print(verification)



if __name__ == '__main__':
    load_config()
    main()
