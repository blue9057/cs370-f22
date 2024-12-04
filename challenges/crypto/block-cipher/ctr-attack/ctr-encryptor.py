#!/usr/bin/env python2

# import pycryptodome
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter
from Crypto.Random.random import _r

# import pwntools
from pwn import *

from user import User

# for printing purpose
msg_id = ['uid', 'username', 'password', 'message 0', 'message 1', 'message 2', 'is_admin']
iv_msg_id = ['nonce'] + msg_id


# The main function that runs encryption
def main():

    # get a random key
    key = Random.get_random_bytes(16)
    # get a random nonce
    nonce = _r.getrandbits(128)

    print("\n\nA random key: %s" % repr(key.encode('hex')))
    print("\n\nA random nonce: %s" % repr("%32x" % nonce))

    # TODO: read the user creation
    # create a user
    u = User()

    # uid 1, username notadministrator, password passwordpassword
    u.uid = 1
    u.username = 'notadministrator'
    u.password = 'passwordpassword'
    # a template message
    u.message = 'The sky is blue, cs370 crypto is a boring class.'
    # not an admin at all. it must be non-zero to be an admin
    u.is_admin = 0

    # serialize the object (transform the object into a string)
    data = str(u)

    # print the raw data before applying encryption, per each block
    print("\n\nData before encryption (raw, 16-byte in each row):")
    per_16_byte = [data[i*16:i*16+16] for i in range(len(data)/16)]
    for i in range(len(per_16_byte)):
        print("%s\t\t <= %s" % (repr(per_16_byte[i]), msg_id[i]))

    # print the hex format of the data before applying encryption, per each block
    print("\n\nData before encryption (hex, 16-byte in each row):")
    per_16_byte = [data[i*16:i*16+16] for i in range(len(data)/16)]
    for i in range(len(per_16_byte)):
        print("%s\t\t <= %s" % (repr(per_16_byte[i].encode('hex')), msg_id[i]))


    # TODO: read how the encryption works
    # Apply AES-CTR-128 with the (key, nonce) to the data

    # create a counter function (increments the counter as the encryption runs by)
    counter = Counter.new(128, initial_value=nonce)
    # set key and the counter to initialize AES-CTR-128
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    # transform the nonce from integer to bytes
    byte_nonce = ("%32x" % nonce).decode('hex')
    # ciphertext includes byte-string nonce at the head
    encrypted = byte_nonce + cipher.encrypt(data)

    # print the raw byte strings of the encrypted data per each block
    print("\n\nData after encryption (raw, 16-byte in each row):")
    per_16_byte = [encrypted[i*16:i*16+16] for i in range(len(encrypted)/16)]
    for i in range(len(per_16_byte)):
        print("%s\t\t <= %s" % (repr(per_16_byte[i]).ljust(66, ' '), iv_msg_id[i]))

    # print the hex format of the encrypted data per each block
    print("\n\nData after encryption (hex, 16-byte in each row):")
    per_16_byte = [encrypted[i*16:i*16+16] for i in range(len(encrypted)/16)]
    for i in range(len(per_16_byte)):
        print("%s\t\t <= %s" % (repr(per_16_byte[i].encode('hex')), iv_msg_id[i]))


    # write the encrypted data as encrypted.user
    try:
        with open("encrypted.user", "wb") as f:
            f.write(encrypted)
    except:
        print("Failed to write encrypted.user")

    # write the key for later use (you can't read this)
    try:
        with open("key", "wb") as f:
            f.write(key)
    except:
        print("Failed to write key")


if __name__ == '__main__':
    main()
