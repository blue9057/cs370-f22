#!/usr/bin/env python2

from Crypto.Cipher import AES
from Crypto import Random

from user import User

flags = []
key_path = flag_path = ''

def load_flags():
    global flags
    try:
        with open(flag_path, "rb") as f:
            flags = [line.strip() for line in f.readlines()]
    except:
        print("Failed to load the flags")
        quit()

def load_key():
    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except:
        print("Failed to open the key")
        quit()

    return key

def read_file(filename):
    try:
        with open(filename, "rb") as f:
            data = f.read()
    except:
        print("File not found!")
        quit()

    return data

def print_menu():
    print("\nChoose which flag do you want to get:")
    print("1. I made uid == 0 (super user)")
    print("2. I made is_admin == 1")
    print("3. I changed the password to something else")
    print("4. quit")


def get_the_choice(message):
    choice = 0
    while True:
        print_menu()
        choice = raw_input(message)
        try:
            int_choice = int(choice)
            if (int_choice >= 1 and int_choice <= 4):
                break
            else:
                print("Incorrect choice.. (not in 1..4)")
        except:
            print("Incorrect choice.. (not int)")
            pass

    return int_choice


# TODO: read this; flag releasing conditions
def handle_flag_1(u):
    print("For flag 1")
    print("User's uid == %d" % u.uid)

    # TODO: you need to make u.uid == 0 to get the first flag!
    if u.uid == 0:
        print("You made its uid == 0! Reward is flag 1!")
        print(flags[0])
    else:
        print("Your uid is not 0 yet...")

def handle_flag_2(u):
    print("For flag 2")
    print("User's is_admin == %d" % u.is_admin)

    # TODO: you need to make u.is_admin == 1 to get the second flag!
    if u.is_admin == 1:
        print("You made it as an admin! Reward is flag 2!")
        print(flags[1])
    else:
        print("You are not admin yet... make the value as 1!")

def handle_flag_3(u):
    print("For flag 3")
    password = raw_input("Type your password: ")
    password = password.strip()
    print("Your password is %s" % password)

    # TODO: you need to make u.is_admin == 1 to get the second flag!
    if u.password == password:
        print("Your password is equal to user's password")
        if u.password == 'passwordpassword':
            print("u.password is still the same, not changed!")
            print("No flag")
        else:
            print("You have changed the password and know what it is!")
            print("Reward is the flag 3")
            print(flags[2])

# TODO: read this function and follow the execution
def menu(u):

    # ask you a choice
    int_choice = get_the_choice("Your choice (1-4): ")

    # each choice (1,2,3) will handle the flag condition checking
    if int_choice == 1:
        handle_flag_1(u)
    elif int_choice == 2:
        handle_flag_2(u)
    elif int_choice == 3:
        handle_flag_3(u)
    elif int_choice == 4:
        quit()


# TODO: read this function first
def main():

    # load 3 flags securely
    load_flags()

    # load the decryption key
    key = load_key()
    print("Key was loaded successfully!")
    # don't print the key in the release mode
    #print("Key: %s" % key.encode('hex'))

    # get the filename of the encrypted user object
    filename = raw_input("Give me the filename of your encrypted object: ")
    encrypted_data = read_file(filename)

    # run decryption
    cipher = AES.new(key, AES.MODE_ECB)
    data = cipher.decrypt(encrypted_data)
    # load decrypted data as a user object
    u = User()
    u.load(data)

    # print data
    print("Decrypted user information:")
    print("%10s \t: %s" % ('uid', repr(u.uid)))
    print("%10s \t: %s" % ('username', repr(u.username)))
    print("%10s \t: %s" % ('password', repr(u.password)))
    print("%10s \t: %s" % ('message', repr(u.message)))
    print("%10s \t: %s" % ('is_admin', repr(u.is_admin)))
    print("\nRaw data: %s\n" % repr(data))

    # TODO: read menu function
    menu(u)

def load_config():
    global key_path, flag_path
    try:
        with open("config", "rb") as f:
            path = f.readline().strip()
            key_path = "%s/key" % path
            flag_path = "%s/flags" % path
    except:
        print("failed to load the config")
        quit()

if __name__ == '__main__':
    load_config()
    main()
