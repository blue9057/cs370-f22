#!/usr/bin/env python2

from Crypto.Cipher import AES
from Crypto import Random

# The main function that runs encryption
def main():

    # open the password word lists
    with open("password-list.txt", "rb") as f:
        _passwords = f.readlines()
        passwords = [password.strip()[:16] for password in _passwords]

    # open the encrypted flag
    with open("encrypted_flag", "rb") as f:
        data = f.read()

    # break it as an IV and the encrypted data
    iv = data[:16]
    encrypted_data = data[16:]

    # for each password in the list
    for password in passwords:
        # set the key with the password
        key = '%16s' % password

        # how can we create AES-CBC cipher in Python?
        # how can we initialize that with key and the iv?
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # how can we decrypt encrypted_data with the AES cipher object?
        decrypted = cipher.decrypt(encrypted_data)

        # correctly decrypted flag starts with 'cs370{'
        # can you check if the decrypted result is correct or not?
        # how?
        if decrypted[0:5] == 'cs370':
            print("Key found: %s" % key)
            print(decrypted)
            break

if __name__ == '__main__':
    main()
