#!/usr/bin/env python

# import pwntools, a tool to interacting with a binary program via stdin/stdout
# https://docs.pwntools.com/en/stable/
from pwn import *

# open the process, the target program ./caesar
p = process('./caesar')

# read the welcome message and print
# recvline will receive text until it sees the newline (includes '\n')
# and then strip() will remove the tailing newline.
print(p.recvline().strip())

# read the ciphertext
cipher_text = p.recvline().strip()
# print the ciphertext
print("ciphertext %s" % (cipher_text))

# read the text that asks plaintext, 'Give me your plaintext:\n'
print(p.recvline().strip())

# TODO: write your decrypt function here
def decrypt(ciphertext):
    # update this plaintext as a correct decryption of the ciphertext
    plaintext = ''

    # TODO: finish decryption here
    # Hint: ord('a') == 97
    #       chr(97) == 'a'
    #       ord('A') == 65
    #       chr(65) == 'A'
    #       ord('c') - ord('a') == 99 - 97 == 2
    #
    #       So, ord(character) returns the byte value (as integer) of the
    #       character, and chr(x) returns the character string of the
    #       integer value x.
    #
    #       The following code will safely offsetting a character if
    #       The a_character is in range of A-Z
    #       chr((ord(a_character) - ord('A') + offset + 26) % 26 + ord('A'))
    # for each character of ciphertext
    for c in ciphertext:
        # if the character is in the range of a-z
        if c >= 'a'[0] and c <= 'z'[0]:
            # TODO: fix this
            plaintext += c
        # if the character is in the range of A-Z
        elif c >= 'A'[0] and c <= 'Z'[0]:
            # TODO: fix this
            plaintext += c
        # if the character is not in A-Z nor a-z
        else:
            plaintext += c

    return plaintext

plain_text = decrypt(cipher_text)
print("My plaintext: %s" % (plain_text))

p.sendline(plain_text)

# interact with the program via console. let's see whatever the program says!
p.interactive()
