#!/usr/bin/env python2

from Crypto.Hash import SHA256

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


# TODO: read this function first
def main():
    # load 3 flags securely
    load_flags()

    print("""Please provide a file that stores:
            [ content-of-encrypted.user ][ HMAC of encrypted.user ]""")
    print("Use SHA256( SHA256(K) + data ) as HMAC, where key is cs370")
    # get the filename of the encrypted user object
    filename = raw_input("Give me your filename: ")
    encrypted_mac_data = read_file(filename)

    hmac = encrypted_mac_data[-32:]
    encrypted_data = encrypted_mac_data[:-32]

    h = SHA256.new()
    h.update('cs370')
    h_key = h.digest()

    print("I am using the key 'cs370', and the hash of my key in hex is:")
    print(h_key.encode('hex'))

    h = SHA256.new()
    h.update(h_key + encrypted_data)
    h_mac = h.digest()

    print("My calculated HMAC is: %s" % h_mac.encode('hex'))
    print("Your provided HMAC is: %s" % hmac.encode('hex'))

    if h_mac == hmac:
        print("Two MACs are equal, you are good to go!")
        print(flags)
    else:
        print("Wrong MAC")


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
