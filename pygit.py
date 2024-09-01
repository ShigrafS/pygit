import argparse, collections, difflib, enum, hashlib, operator, os, stat
import struct, sys, time, urllib.request, zlib

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

#Initializing Repository
def init(repo):
    #Cre4ating a directory for repository and initializing directory
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.git'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo,'.git',name))

    write_file(os.path.join(repo,'.git','HEAD'), b'ref: refs/heads/main')
    
    print("Initialized empty repository: {}".format|(repo))

def hash_object(data, obj_type, write=True):
    #Compute the hash of the object data
    header = '{}{}'.format(obj_type, len(data)).encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            write_file(path, zlib.compress(full_data))
    return sha1