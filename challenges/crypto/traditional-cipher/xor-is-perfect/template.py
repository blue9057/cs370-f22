#!/usr/bin/env python

from pwn import *

p = process("./xor-is-perfect")

# get some intro lines
print(p.readline().strip())
print(p.readline().strip())
print(p.readline().strip())
print(p.readline().strip())
print(p.readline().strip())

# get plaintext
plaintext = p.readline().strip()
print('plaintext: %s' % plaintext)

# get some useless lines
print(p.readline().strip())
print(p.readline().strip())

# get ciphertext
ciphertext = p.readline().strip()
print('ciphertext: %s' % ciphertext)
# get newline
print(p.readline().strip())

# decode plain and the ciphertext from hexcode to byte
byte_plaintext = plaintext.decode('hex')
byte_ciphertext = ciphertext.decode('hex')

# print each of them
print(byte_plaintext)
print(byte_ciphertext)

# we will store the key as integers
key = []

print(p.readline().strip())

# get the secret number
secret_number = p.readline().strip()
print('secret_number: %s' % secret_number)
# get the byte of the secret number
byte_secret_number = secret_number.decode('hex')

plain_secret_array = []

# write your code to get the plaintext of the secret numbers and on
