import argparse, collections, difflib, enum, hashlib, operator, os, stat
import struct, sys, time, urllib.request, zlib

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

#Initializing Repository
def innit(repo):
    #Cre4ating a directory for repository and initializing directory
    os.mkdir(repo)
    os.mkdir(os.path.join(repo, '.git'))
    for name in ['objects', 'refs', 'refs/heads']:
        os.mkdir(os.path.join(repo,'.git',name))

    write_file(os.path.join(repo,'.git','HEAD'), b'ref: refs/heads/main')
    
    print("Initialized empty repository: {}".format|(repo))