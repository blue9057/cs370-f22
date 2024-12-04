#!/usr/bin/env python3

import os
import glob
import sys

ROOT = os.path.dirname(__file__)

LAB_CAL = """
"""

# Not released
"""
Crackme
Stack Overflow
Writing Shellcode
Bomb Lab2 / Shellcode
Stack Overflow
>
# NSA Codebreaker Challenge
Bypassing Stack Protection
Bypassing DEP/ASLR
Return-oriented Programming
>
Remote Attacks
>
Exploiting Misc1 (int-ovfl, race, tictou &c)
Exploiting Heap Bugs
# # tutorial: fuzzing
# Exploiting Misc2 (bypassing sandbox, kernel exploits &c) (Alternative: Web Exploitation)
# >
# Realworld Exploit
# Fuzzing
# Symbolic Execution
# Exploit Real Bugs
# Exploiting Kernel
# Crypto Challenges
"""

def patching(out):
    # out = out.replace("Thr\n- Due: Lab 03", "")
    # out = out.replace("Thr\n- Due: Lab 04", "Thr\n- Due: Lab 03")
    # out = out.replace("Thr\n- Due: Lab 11", "Thr\n- Due: Lab 04/10/11")
    # out = out.replace("Wed\n- Rec: Lab 03",
    #                   "Wed\n- Rec: [https://codebreaker.ltsnet.net/content/codebreaker3_techtalk_v6.pdf" +
    #                   " Lab 03: Last Year's Challenges]" )
    # out += "Thr\n- Due: Lab 04/11"
    return out

def dump_cal():
    out = []
    week = 1
    due = []
    for l in LAB_CAL.splitlines():
        l = l.strip()
        if l == "" or l.startswith("#"):
            continue

        if l.startswith(">"):
            out.append("Thr\nFri\n")
            continue

        if len(due) != 0:
            out += due
            due = []

        # assign
        README = glob.glob("%s/lec/lab%02d-*/README-lab.txt" % (ROOT, week))
        if len(README) == 1:
            link = README[0].replace("%s/lec/" % ROOT, "l/")
            out.append("Tue")
            out.append("- Assign: [%s Lab %02d: %s]" % (link, week, l))
        else:
            out.append("Tue")
            out.append("- Assign: Lab %02d: %s" % (week, l))

        if (week > 2):
            due.append("- Due: Lab %02d" % (week-1))

        # due
        #due.append("Wed")
        #due.append("- Rec: Lab %02d" % week)

        #if(week > 1):
        #  due.append("Tue")
        #  due.append("- Due: Lab %02d" % (week-1))
        week += 1

    return patching("\n".join(out))

if __name__ == '__main__':
    print(dump_cal())
