#!/usr/bin/env python2

target_path = '/home/labs/crypto/ctr-attack'
target_level = 'week1-level6-solved'

files_to_copy = ['ctr-decryptor.py', 'ctr-encryptor.py',
        'flags', 'key', 'launcher', 'output.txt', 'encrypted.user',
        'user.py', 'template.py']

protected = ['flags', 'key', 'launcher']
suid_target = 'launcher'
target_script = 'ctr-decryptor.py'

import os

# create directory
if not os.path.exists(target_path):
    os.system("sudo mkdir %s" % target_path)

# copy files
for filename in files_to_copy:
    os.system("sudo cp %s %s/%s" % (filename, target_path, filename))

# protected privilege
for filename in protected:
    os.system("sudo chown root:%s %s/%s" % (target_level, target_path, filename))
    os.system("sudo chmod 440 %s/%s" % (target_path, filename))

# set suid
os.system("sudo chmod 2755 %s/%s" % (target_path, suid_target))
os.system("sudo touch %s/config" % (target_path))
os.system("sudo chmod 666 %s/config" % (target_path))

with open("%s/config" % (target_path), 'wb') as f:
    f.write("%s\n" % target_path)
    f.write("%s\n" % target_script)

os.system("sudo chown root:%s %s/config" % (target_level, target_path))
os.system("sudo chmod 440 %s/config" % (target_path))