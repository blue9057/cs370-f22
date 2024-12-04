================
Lab Instructions
================

--------
Overview
--------
In each assignment set, you are asked to solve a set of challenges
(typically 5~10 challenges).
In each challenge, you have to submit the flag and a write-up
via `scoreboard <https://ctf.unexploitable.systems>`__:
the flag you got from the challenge
and the write-up that summarizes how you get the flag (see below).

A flag is an ASCII string that matches with a regular expression of cs370{[^\}]+},
and you can find it either in the challenge program or
in the challenge directory (usually as a 'flag' file).
Your job is to read this flag by following the instructions of the challenge.

For example, some cryptography challenges require you to break
a weak cryptography scheme and read the plaintext data
even without knowing the key, and that plaintext data
would be the flag.

Otherwise, you need to understand how the challenge program works,
and then, fool the program to read-out the flag for you.

Most of flags are stored (in)securely as `flag` file.

--------------------------------
Taking actions #1 (Registration)
--------------------------------

1) Register your account

- Visit the submission site: `here
  <https://ctf.unexploitable.systems>`_. You
  will use the **registration menu**.
  Please use @oregonstate.edu e-mail address; otherwise,
  you cannot register to the scoring system.

2) Verify your account. Please check Junk/Spam folder if you cannot
get the e-mail message from the server. The title of the confirmation message is:
`Message from CS 370 Introduction to Security`, and
it will be coming from the address `postmaster@unexploitable.systems`.


2) You need to register your SSH public key to our web scoring system.
   Please register yourself at https://ctf.unexploitable.systems/ first,
   and then, go to the 'Account' page (see the top bar in the website),
   and take the following steps on the flip server to register a server account:

.. code-block:: bash

    # please log-in to the flip server first.

    # create a new ed25519 key
    [filp] $ ssh-keygen -t ed25519
    Generating public/private ed25519 key pair.

    # select your key location
    Enter file in which to save the key (/home/YOUR_ID/.ssh/id_ecdsa):
    => If you don't know what it is, just press the ENTER key 3~4 times.
    Otherwise, type YOUR_KEY_LOCATION to store the new key.

    # type password (you can use an empty one by pressing ENTER, if you wish)
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:

    # check your key location
    Your identification has been saved in YOUR_LOCATION (default: ~/.ssh/id_ed25519)
    Your public key has been saved in YOUR_LOCATION (default: ~/.ssh/id_ed25519)

    # After key generation
    [flip] $ cat ~/.ssh/id_ed25519.pub
    # -> copy and paste the key, use this key to register your server account
    # or use YOUR_KEY_LOCATION/id_ed25519.pub file to get the public key.

    # an example of a public key
    ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIONLM0cVwr1u1qE5DtbjnP1c4sQqYRXbXMZnXmw2mq4b blue9057@os-gitlab.com

Do not forget where you store your private key and the passphrase for it.
After having public/private key pair, please register your server account
at `here <https://ctf.unexploitable.systems/register_account>`__:

Please use all lowercase username (e.g., red9057) for the username.


3) Connect to the course server

.. code-block:: bash

    # login to flip first

    # login to the course server. Replace the YOURID part to your server username
    [flip] $ ssh YOURID@vm-ctf1.eecs.oregonstate.edu
    e.g., ssh red9057@vm-ctf1.eecs.oregonstate.edu

    # In case if you placed your id_ed25519 to YOUR_KEY_LOCATION, then
    [flip] $ ssh -i YOUR_KEY_LOCATION/id_ed25519 YOURID@vm-ctf1.eecs.oregonstate.edu

    # let's start login challenge
    [CTF_server] $ cd /home/labs/login-flag
    [CTF_server] $ cat flag


5) Submit your solution and flag

.. code-block:: bash

    # Submit Flag
      1) Visit the scoring website
         https://ctf.unexploitable.systems

      2) Choose the challenge name from the correct challenge set

      3) Submit the flag!

    # Submit Writeup
      (will be announced later)

    # NOTE. you don't get an actual score until you submit writeup
    # NOTE. you can also submit your flag and writeup through the class website


---------------
Write-up sample
---------------

.. code-block:: c

    This assignment demonstrates a weakness of the Electronic Code Book (ECB)
    mode of the block cipher. Although the cryptographic scheme, the Advanced
    Encryption Standard (AES) encrypted the bitmap data correctly, in the ECB
    mode, the same plaintext data block will be encrypted as the fixed
    ciphertext, and thereby, we can identify the patterns of plaintext for
    the same blocks in the ciphertext. As a result, even though the bitmap
    data were encrypted, we can read the hidden text in the plaintext picture
    because ciphertext block pattern leaks the plaintext block patterns.
