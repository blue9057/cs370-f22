#!/usr/bin/env python2

import os

from Crypto.Hash import SHA256


def main():

    os.system("xxd encrypted.user")

    # read the encrypted data from the file encrypted.user
    with open("encrypted.user", "rb") as f:
        encrypted_data = f.read()

    # We will calculate H(H(key) + encrypted_data)
    # H here is SHA256
    # key here is cs370

    # Compute H(key) first
    # create an SHA256 object
    h = SHA256.new()
    # put our key
    key = 'cs370'
    # update hash with the key as a message
    h.update(key)
    # Generate hash to get H(key)
    h_key = h.digest()
    print("H(key) == H('cs370'):")
    print(h_key.encode('hex'))

    # create a new hash object
    h = SHA256.new()
    # TODO: construct message, H(key) + encrypted_data
    message = ''
    # update hash with the message for HMAC
    h.update(message)
    # the resulting hash is HMAC = H(H(key) + encrypted_data)
    hmac = h.digest()
    print("HMAC(encrypted_data) = H(H(K) + encrypted_data):")
    print(hmac.encode('hex'))

    # will be stored in hmac.user
    with open("hmac.user", "wb") as f:
        f.write(encrypted_data + hmac)

    os.system("xxd hmac.user")

if __name__ == '__main__':
    main()
