#!/usr/bin/env python2

import random
from Crypto.Cipher import AES

key = ("%016d" % (random.randint(1,1000000000000000000)))[:16]

cipher = AES.new(key, AES.MODE_CBC, '0'*16)

with open('ecb.bmp', 'rb') as f:
    data = f.read()

header = data[:90]
rest = data[90:]

msg = cipher.encrypt(rest)

with open('encrypted-cbc.bmp', 'wb') as f:
    f.write(header)
    f.write(msg)
