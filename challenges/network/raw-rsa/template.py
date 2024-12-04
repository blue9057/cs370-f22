#!/usr/bin/env python2

from pwn import *

def rprint(string):
    print(string.rjust(80))

def solve_game(p):
    ##########################################################################
    # DO NOT EDIT                                                            #
    ##########################################################################
    str_public_keys = p.readline().strip()
    print(str_public_keys)
    pks = str_public_keys.split(':')[1].strip().split(',')
    N, e = [int(s.split('=')[1].strip()) for s in pks]
    print("Received N %d e %d" % (N, e))

    # get the encrypt quiz message
    quiz = p.readline().strip()
    print(quiz)
    quiz_number = int(quiz.split(':')[1].strip())
    print('Number to be encrypted: %d' % quiz_number)
    ##########################################################################

    # TODO: encrypt the quiz number and send back to the program
    # e.g., Please encrypt the following number and send back to me: 193
    # HINT: use pow(m, e, N), where m is the plaintext message
    result = pow(1, 1, 1)   # edit this line
    rprint("Encrypted number %d" % result)
    p.sendline(str(result))


    ##########################################################################
    # DO NOT EDIT                                                            #
    ##########################################################################
    # read...
    msg = p.readline().strip()
    print(msg)
    if not 'Correct' in msg:
        print("Your encryption was incorrect")
        quit()

    # get the private key, d is the private key
    pvk_string = p.readline().strip()
    print(pvk_string)
    d = int(pvk_string.split(':')[1].split('=')[1].strip())
    print("Received d %d" % d)

    # get the decrypt quiz message
    quiz = p.readline().strip()
    print(quiz)
    quiz_number = int(quiz.split(':')[1].strip())
    print('Number to be decrypted: %d' % quiz_number)
    ##########################################################################

    # TODO: encrypt the quiz number and send back to the program
    # e.g., Please encrypt the following number and send back to me: 193
    # HINT: use pow(c, d, N), where c is the ciphertext message
    result = pow(1, 1, 1) # edit this line
    rprint("Decrypted number %d" % result)
    p.sendline(str(result))

    ##########################################################################
    # DO NOT EDIT                                                            #
    ##########################################################################
    # read...
    msg = p.readline().strip()
    print(msg)
    if not 'Correct' in msg:
        print("Your encryption was incorrect")
        quit()
    ##########################################################################


# TODO: the program starts at here..
def main():
    p = process("./rsa.py")

    # read intro messages
    print(p.readline().strip())
    print(p.readline().strip())

    # run 10 games
    for i in range(10):
        solve_game(p)
        raw_input("Press ENTER to continue...")

    # will get the flag after the game finishes
    p.interactive()


if __name__ == '__main__':
    main()
