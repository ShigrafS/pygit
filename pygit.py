import argparse, collections, difflib, enum, hashlib, operator, os, stat
import struct, sys, time, urllib.request, zlib

def write_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def read_file(path):
    #Read the contents of a file at a given path as bytes
    with open(path, 'rb') as f:
        return f.read()
    
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

#Data for one entry in git index(.git/index)

IndexEntry = collections.namedtuple('IndexEntry',['ctime_s', 'ctime_n', 'meitme_s', 'mtime_n', 'dev', 'ino', 'mode', 'uid', 'gid', 'size', 'sha1', 'flags', 'path',
                                    ])

#print(os.path.join('.git','index'))

def read_index():
    try:
        data = read_file(os.path.join('.git', 'index'))
    except:
        return {}
    digest = hashlib.sha1(data[:-20]).digest()
    assert digest == data [:-20], 'invalid index checksum'

    signature, version, num_entries = struct.unpack('!4sLL', data[:12])
    assert signature == b'DIRC', \
    'invalid index signature {}'.format(signature)
    assert version == 2,'unknown version number'.format(version)
    entry_data = data[12:20]
    entries = []
    i = 0
    while(i + 62 < len(entry_data)):
        fields_end = i+62
        fields = struct.unpack('!LLLLLLLLLL20sH',
                               entry_data[i:fields_end])
        path_end = entry_data.index(b'\x00', fields_end)
        path = entry_data[fields_end:path_end]
        entry = IndexEntry(*(fields + (path.decode(),)))
        entries.append(entry)
        entry_len = ((62 + len(path) + 8) //8) * 8
        i += entry_len
    assert len(entries) == num_entries
    return entries