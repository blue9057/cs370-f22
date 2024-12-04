#!/usr/bin/env python2

from Crypto.Cipher import AES
from Crypto import Random

from user import User

# for printing purpose
msg_id = ['uid', 'username', 'password', 'message 0',
            'message 1', 'message 2', 'is_admin']
iv_msg_id = ['iv'] + msg_id

# The main function that runs encryption
def main():

    # get a random key
    key = Random.get_random_bytes(16)
    # key will be masked in the output.txt
    print("\n\nA random key: %s" % repr(key.encode('hex')))


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
    # FYI, the encryption scheme will not use padding, and the User object
    # is with exactly 7 blocks so it will be 112 bytes (16 * 7).

    # Apply AES-ECB-128 with the key to the data
    cipher = AES.new(key, AES.MODE_ECB)
    # encrypted data is ciphertext of each block of plaintext data
    encrypted = cipher.encrypt(data)


    # print the raw byte strings of the encrypted data per each block
    print("\n\nData after encryption (raw, 16-byte in each row):")
    per_16_byte = [encrypted[i*16:i*16+16] for i in range(len(encrypted)/16)]
    for i in range(len(per_16_byte)):
        print("%s\t\t <= %s" % (repr(per_16_byte[i]).ljust(66, ' '), msg_id[i]))

    # print the hex format of the encrypted data per each block
    print("\n\nData after encryption (hex, 16-byte in each row):")
    per_16_byte = [encrypted[i*16:i*16+16] for i in range(len(encrypted)/16)]
    for i in range(len(per_16_byte)):
        print("%s\t\t <= %s" % (repr(per_16_byte[i].encode('hex')), msg_id[i]))


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
