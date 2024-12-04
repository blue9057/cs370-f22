#!/usr/bin/env python2

from Crypto.Cipher import AES
from Crypto import Random

# The main function that runs encryption
def main():

    # get a random key
    key = '%16s' % '??????????'

    # get a random IV
    iv = Random.get_random_bytes(16)

    print("\n\nA chosen key: %s" % repr(key))
    print("\n\nA random iv: %s" % repr(iv.encode('hex')))

    try:
        with open("flag", "rb") as f:
            data = f.read()
    except:
        print("Cannot open file flag")
        quit()

    # TODO: read how the encryption works
    # Apply AES-CBC-128 with the (key, iv) to the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # IV is attached to the head of the encrypted data
    encrypted = iv + cipher.encrypt(data)

    # write it as an encrypted_flag
    try:
        with open('encrypted_flag', 'wb') as f:
            f.write(encrypted)
    except:
        pass


if __name__ == '__main__':
    main()
