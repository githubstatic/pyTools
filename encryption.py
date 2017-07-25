#!/user/bin/python
#Filename:encryption.py

#this is a integration of some encrypt algorithm

import hashlib

def encrypt(data, type):
    if type=="md5":
        md5 = hashlib.md5()
        md5.update(data)
        return md5.hexdigest()
    elif type=="sha1":
        sha = hashlib.sha1()
        sha.update(data)
        return sha.hexdigest()
    elif type=="sha224":
        sha = hashlib.sha224()
        sha.update(data)
        return sha.hexdigest()
    elif type=="sha256":
        sha = hashlib.sha256()
        sha.update(data)
        return sha.hexdigest()
    elif type=="sha384":
        sha = hashlib.sha384()
        sha.update(data)
        return sha.hexdigest()
    elif type=="sha512":
        sha = hashlib.sha512()
        sha.update(data)
        return sha.hexdigest()
    else:
        return False

def modelName():
    return __name__
