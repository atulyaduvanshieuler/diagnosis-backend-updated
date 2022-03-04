from pickletools import bytes8
import hashlib


def converter(string):
    
    bytes_string = string.encode()
    res = hashlib.sha256(bytes_string).hexdigest()
    return res
