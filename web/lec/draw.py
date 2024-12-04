#!/usr/bin/env python3


import matplotlib.pyplot as plt
import random

arr = []
arrk = []
arre = []
for i in range(100):
    arr.append(i)
    r = random.randint(1,100)
    arrk.append(r)
    arre.append(i^r)


plt.plot(arr)
plt.ylabel('sequential')
plt.show()

plt.plot(arrk)
plt.ylabel('random keys')
plt.show()

plt.plot(arre)
plt.ylabel('XOR Cipher')
plt.show()
