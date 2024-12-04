#!/usr/bin/env python2

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

# TODO: read this function first
def main():
    # load the flag securely

    print("RSA TEST")

    # create an RSA private key; let's create a secure one.
    # Internally, pycryptodome will use secure random source to create a key
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()

    pem_pvk = private_key.export_key('PEM')
    print("Your RSA private key:\n")
    print(pem_pvk)

    # your public key is stored at my_public_key.pem
    with open("my_public_key.pem", "wb") as f:
        f.write(public_key.export_key('PEM'))

    # TODO: read the following code to learn how to encrypt/decrypt data..
    # create a PKCS1_OAEP cipher for
    # public key : encryption and verify
    # private key: decryption and signing
    cipher_rsa_public = PKCS1_OAEP.new(public_key)
    cipher_rsa_private = PKCS1_OAEP.new(private_key)

    # You will encrypt "Hello CS370"
    string = 'Hello CS370'

    # Encryption must be with a public key (encrypt)
    ciphertext = cipher_rsa_public.encrypt(string)

    print("\nYour encrypted data: ")
    print(ciphertext.encode('hex'))

    # Decryption must be with a private key (decrypt)
    print("\nYour decrypted data: ")
    print(cipher_rsa_private.decrypt(ciphertext))
    print("\n\n")


    # You will get a SHA256 fingerprint of the string and encrypt it!
    sha256 = SHA256.new()
    sha256.update(string)
    fingerprint = sha256.digest()
    ciphertext = cipher_rsa_public.encrypt(fingerprint)

    print("\nYour encrypted data: ")
    print(ciphertext.encode('hex'))
    print("\nYour decrypted data: ")
    print(cipher_rsa_private.decrypt(ciphertext).encode('hex'))
    print("\nOriginal SHA256 sum: ")
    print(fingerprint.encode('hex'))
    print("\n\n")

    # TODO: Can you sign the following message? Please do:
    #       1: get an SHA256 fingerprint of the message, likewise we did
    #          in the example above
    #       2: encrypt the digest() of the SHA256 using the private key.
    #          encrypt using private key is 'signing', because only
    #          you can generate this encrypted message while all the others
    #          can decrypt it

    string = 'CS370 Introduction to Security'
    signer = PKCS115_SigScheme(private_key)

    # 1. Get an SHA256 fingerprint of the message, e.g.,
    # sha = SHA256.new()
    # sha.update(string)
    # fingerprint = sha.digest()
    # TODO: your code here
    sha = SHA256.new(string)

    # 2. Get the signature using signer.sign(fingerprint)
    #    and store it in the signature variable
    # TODO: your code here
    signature = signer.sign(fingerprint)
    print(signature)



    with open("signature", "wb") as f:
        f.write(signature)

    if len(signature) < 250:
        print("Error, RSA signature was not there...")
        quit()
    else:
        print("Your signature: ")
        print(signature.encode('hex'))

    print("Your signature has been written, and please run the ./launcher")



    # 1. Get an SHA256 fingerprint of the message, e.g.,
    # sha = SHA256.new()
    # sha.update(string)
    # fingerprint = sha.digest()
    # TODO: your code here
    sha = SHA256.new()
    sha.update(string)
    fingerprint = sha.digest()

    # 2. Get the signature using cipher_rsa_private.encrypt(fingerprint)
    #    and store it in the signature variable
    # TODO: your code here
    signature = cipher_rsa_private.encrypt(fingerprint)



    with open("signature", "wb") as f:
        f.write(signature)

    if len(signature) < 250:
        print("Error, RSA signature was not there...")
        quit()
    else:
        print("Your signature: ")
        print(signature.encode('hex'))

    print("Your signature has been written, and please run the ./launcher")


if __name__ == '__main__':
    main()
