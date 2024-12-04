#!/usr/bin/env python2
# we use python2 in vm-ctf1 server

# import means including some pre-written libraries.
# below, we include os and sys libraries.
import os
import sys


# suppose we have a hexadeximal string (32 digits, 16-bytes)
hex_string = "8090a0b0c0d0e0f08595a5b5c5d5e5f5"
print("hex_string: %s" % repr(hex_string))

# to change this as a byte string, we use .decode('hex')
byte_string = hex_string.decode('hex')
# repr returns the variable's representation
print("byte_string: %s" % repr(byte_string))

# byte_string is: '\x80\x90\xa0\xb0\xc0\xd0\xe0\xf0\x85\x95\xa5\xb5\xc5\xd5\xe5\xf5'
# to change this byte_string as an integer array
# we run the list comprehension (a python's syntax)

# this will generate byte array, e.g., ["\x80", "\x90", ...]
byte_array = [c for c in byte_string]
print("byte_array: %s" % repr(byte_array))

# c was a byte, e.g., "\x80". To change this to integer 0x80,
# we can use ord(c), 0x80 == ord("\x80"), 0x41 == ord('A')
int_array = [ord(c) for c in byte_string]
print("int_array: %s" % repr(int_array))


# prepare a 16 byte key
xor_key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf]


# let's apply an xor encryption to the array for fun
# create an empty array
int_encrypted_array = []

# write a for loop. range(8) means from 0 to 7 and stop at 8
# len(int_array) returns the length of integer array.
# Because we use a 16-byte string, it will be 16.
# So the below means
# for i in range(16): # from 0 to 15 and stop at 16, i indicates the number
for i in range(len(int_array)):
    apply_xor = int_array[i] ^ xor_key[i] # ^ is the xor operation between 2 int
    # .append is a method to add an item to an array
    int_encrypted_array.append(apply_xor)

print("int_encrypted_array: %s" % repr(int_encrypted_array))


# to change an encrypted array to a byte string, we use chr() instead of ord()
# examples:
# chr(0x41) == 'A'
# ord('A') == 0x41
# chr(ord('A')) == 'A'
# ord(chr(0x41)) == 0x41
byte_encrypted_array = [chr(c) for c in int_encrypted_array]
print("byte_encrypted_array: %s" % repr(byte_encrypted_array))

# to change a byte array to byte string, we use ''.join(byte_array)
byte_encrypted_string = ''.join(byte_encrypted_array)
print("byte_encrypted_string: %s" % repr(byte_encrypted_string))

# the result is:
# byte_encrypted_string = '\x80\x91\xa2\xb3\xc4\xd5\xe6\xf7\x8d\x9c\xaf\xbe\xc9\xd8\xeb\xfa'

# to change that byte_string to a hexadecimal string, e.g., 8091a2b3c4d5...
# we use .encode('hex')
hex_encrypted_string = byte_encrypted_string.encode('hex')
print("hex_encrypted_string: %s" % repr(hex_encrypted_string))

# now it prints '8091a2b3c4d5e6f78d9cafbec9d8ebfa'


#
#   After you submit the decrypted secret number back to the program using
#   p.sendline(hex_decrypted_secret_string)
#   try to add 10-ish print(p.readline().strip())
#   then, run the python script, and if it hangs, press Ctrl+C.
#   Then, your python script will generate an exception,
#   and in there, note which line number is problematic for
#   print(p.readline().strip())
#
#   The reason for this exception is that your code try to read some more
#   while the output is not available.
#
#   After removing such unnecessary print(p.readline().strip()), you will
#   see that the last one that was not removed will store the last string
#   that the program prints, say, encrypted flag, etc.
#   then, try to change that line from print(p.readline().strip()) to
#   hex_encrypted_flag = p.readline().strip(), then you have that line
#   in that variable.
#
#   Then, try to print it like print("hex_encrypted_flag: %s" % repr(hex_encrypted_flag))

