#!/usr/bin/env python
import os
import time

while True:
    time.sleep(30)
    os.system("ps aux | grep serve.py | grep -v grep | awk '{print $2}' | xargs kill -9")
    time.sleep(3600*2)
