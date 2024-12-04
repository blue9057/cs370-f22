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

# XXX: Do not share
for i in range(len(byte_plaintext)):
    key.append(ord(byte_plaintext[i]) ^ ord(byte_ciphertext[i]))

# XXX: Do not share
print(key)

print(p.readline().strip())

# get the secret number
secret_number = p.readline().strip()
print('secret_number: %s' % secret_number)
# get the byte of the secret number
byte_secret_number = secret_number.decode('hex')

# XXX: DO not shaare decrypt
plain_secret_array = []

for i in range(len(byte_secret_number)):
    plain_secret_array.append(chr(ord(byte_secret_number[i]) ^ key[i]))

hex_secret_number = ''.join(plain_secret_array).encode('hex')

print(hex_secret_number)
print(p.readline().strip())

# question
print(p.readline().strip())

p.sendline(hex_secret_number)

print(p.readline().strip())
print(p.readline().strip())
print(p.readline().strip())
print(p.readline().strip())

encrypted_flag = p.readline().strip()
print("encrypted_flag: %s" % encrypted_flag)

byte_encrypted_flag = encrypted_flag.decode('hex')

flag_array = []
for i in range(len(byte_encrypted_flag)):
    flag_array.append(chr(ord(byte_encrypted_flag[i]) ^ key[i]))

print(''.join(flag_array))
