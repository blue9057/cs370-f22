#!/usr/bin/env python2

import copy

#######################################################################
#   Some data/functions helpful for the assignment. don't touch!      #
#######################################################################
block_name = ['nonce', 'uid', 'username', 'password', 'message 0',
        'message 1', 'message 2', 'is_admin']

# break it in each block
def cut_in_blocks(encrypted_data):
    length = len(encrypted_data)
    if length % 16 != 0:
        print("Encrypted data length error %d, not divided by 16" % length)

    return [encrypted_data[i*16:i*16+16] for i in range(length/16)]

def convert_int_blocks_to_bytestring(blocks_int):
    return ''.join([''.join([chr(c) for c in a]) for a in blocks_int])

def convert_hex_blocks_to_bytestring(blocks_hex):
    return ''.join([h.decode('hex') for h in blocks_hex])

def convert_bytes_blocks_to_bytestring(blocks_bytes):
    return ''.join(blocks_bytes)


###########################################################################
#   Loading binary data into playable format for you. don't touch and     #
#   just use the arrays that I prepared for you:                          #
#   blocks_bytes, blocks_hex, and blocks_int                              #
###########################################################################

# load the sample encrypted.user
with open("encrypted.user", "rb") as f:
    encrypted_data = f.read()

# blocks_bytes, store data in bytes array, e.g.,
"""
0 (       uid)  : '\xc2\xdcS\x81snq\xeb\xfe\x8a\x05\x01\xf4\xc1B\xe7'
1 (  username)  : '\xb1;b\x80NUMls"\xa5\xe9!\x01\xee\xef'
2 (  password)  : '\xa5\xe2Q\xb5e\x1e\x1f\xfd8u\xcb\xc0 \xd5%\xf4'
3 ( message 0)  : '\xfa\xa3\x02\x84\x99\x89\xc4\x06)\xce\x1e3\xb504\xe4'
4 ( message 1)  : "\xd9H\x00,\xc8^d\xdbk\xf5\xfa@'l\xbe\x94"
5 ( message 2)  : '"\x89\tl\xff\xb9.\x86+\xc3\x9a\xce3B\xaet'
6 (  is_admin)  : '\xb7\xf8g\xdd7\xcf\xeb\x04\xc5~\xe4ST`K\xdc'
"""
blocks_bytes = cut_in_blocks(encrypted_data)
print("Raw bytes")
for i in range(len(blocks_bytes)):
    print("%d (%10s)\t: %s" % (i, block_name[i], repr(blocks_bytes[i])))


# blocks_hex, store each block as hexadecimal digit lines (32 digits), e.g.,
"""
0 (       uid)  : c2dc5381736e71ebfe8a0501f4c142e7
1 (  username)  : b13b62804e554d6c7322a5e92101eeef
2 (  password)  : a5e251b5651e1ffd3875cbc020d525f4
3 ( message 0)  : faa302849989c40629ce1e33b53034e4
4 ( message 1)  : d948002cc85e64db6bf5fa40276cbe94
5 ( message 2)  : 2289096cffb92e862bc39ace3342ae74
6 (  is_admin)  : b7f867dd37cfeb04c57ee45354604bdc
"""
blocks_hex = []
print("Hex")
for byte_str in blocks_bytes:
    blocks_hex.append(byte_str.encode('hex'))
for i in range(len(blocks_hex)):
    print("%d (%10s)\t: %s" % (i, block_name[i], blocks_hex[i]))



# blocks_int, store each byte as int, per each block...
"""
0 (       uid)  : [194, 220, 83, 129, 115, 110, 113, 235, 254, 138, 5, 1, 244, 193, 66, 231]
1 (  username)  : [177, 59, 98, 128, 78, 85, 77, 108, 115, 34, 165, 233, 33, 1, 238, 239]
2 (  password)  : [165, 226, 81, 181, 101, 30, 31, 253, 56, 117, 203, 192, 32, 213, 37, 244]
3 ( message 0)  : [250, 163, 2, 132, 153, 137, 196, 6, 41, 206, 30, 51, 181, 48, 52, 228]
4 ( message 1)  : [217, 72, 0, 44, 200, 94, 100, 219, 107, 245, 250, 64, 39, 108, 190, 148]
5 ( message 2)  : [34, 137, 9, 108, 255, 185, 46, 134, 43, 195, 154, 206, 51, 66, 174, 116]
6 (  is_admin)  : [183, 248, 103, 221, 55, 207, 235, 4, 197, 126, 228, 83, 84, 96, 75, 220]
"""
print("Int")
blocks_int = []
for byte_str in blocks_bytes:
    blocks_int.append([ord(c) for c in byte_str])
for i in range(len(blocks_int)):
    print("%d (%10s)\t: %s" % (i, block_name[i], repr(blocks_int[i])))


# TODO: your tasks are here!!
###########################################################################
#   Read below and use/edit them to generate a program to get flag 1,2,3! #
###########################################################################
# The following functions will convert each blocks array into a bytestring
"""
convert_int_blocks_to_bytestring(blocks_int):
convert_hex_blocks_to_bytestring(blocks_hex):
convert_bytes_blocks_to_bytestring(blocks_bytes)
"""

blocks = {}

def create_file_for_flag_1():
    bytestring = ''

    # use whatever copied array here
    copied_blocks_bytes = copy.deepcopy(blocks_bytes)
    copied_blocks_hex = copy.deepcopy(blocks_hex)
    copied_blocks_int = copy.deepcopy(blocks_int)

    # XXX: Your code here; transform the blocks here

    # in case you used blocks_int
    bytestring = convert_int_blocks_to_bytestring(copied_blocks_int)

    # write as flag1.user
    with open("flag1.user", "wb") as f:
        f.write(bytestring)

def create_file_for_flag_2():
    bytestring = ''

    # use whatever copied array here
    copied_blocks_bytes = copy.deepcopy(blocks_bytes)
    copied_blocks_hex = copy.deepcopy(blocks_hex)
    copied_blocks_int = copy.deepcopy(blocks_int)

    # XXX: Your code here; transform the blocks here

    # in case you used blocks_int
    bytestring = convert_int_blocks_to_bytestring(copied_blocks_int)

    # write as flag2.user
    with open("flag2.user", "wb") as f:
        f.write(bytestring)


# FYI: 16-byte aligned string
"""
The sky is blue,
 cs370 crypto is
 a boring class.                # No, not at all.....
"""
def create_file_for_flag_3():
    bytestring = ''

    # use whatever copied array here
    copied_blocks_bytes = copy.deepcopy(blocks_bytes)
    copied_blocks_hex = copy.deepcopy(blocks_hex)
    copied_blocks_int = copy.deepcopy(blocks_int)

    # XXX: Your code here; transform the blocks here

    # in case you used blocks_int
    bytestring = convert_int_blocks_to_bytestring(copied_blocks_int)

    # write as flag3.user
    with open("flag3.user", "wb") as f:
        f.write(bytestring)


create_file_for_flag_1()
create_file_for_flag_2()
create_file_for_flag_3()
