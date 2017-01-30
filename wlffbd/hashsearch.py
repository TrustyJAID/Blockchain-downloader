# -*- coding: utf-8 -*-
'''Wikileaks hash search functions'''
import json

with open("wlhashes/md5.json", "r") as md5json:
    MD5 = json.load(md5json)
with open("wlhashes/sha1.json", "r") as sha1json:
    SHA1 = json.load(sha1json)
with open("wlhashes/sha256.json", "r") as sha256json:
    SHA256 = json.load(sha256json)


def check_hash(hexcode, sumcheck, MD5=MD5, SHA1=SHA1, SHA256=SHA256):
    '''
    This will return whether or not a wikileaks file hash is inside the blockchain
    '''
    if sumcheck == "md5":
        return ' '.join('{}'.format(key)
                        for key, values in MD5.iteritems()
                        if all(v.lower() in hexcode for v in values))
    if sumcheck == "sha1":
        return ' '.join('{}'.format(key)
                        for key, values in SHA1.iteritems()
                        if all(v.lower() in hexcode for v in values))
    if sumcheck == "sha256":
        return ' '.join('{}'.format(key)
                        for key, values in SHA256.iteritems()
                        if all(v.lower() in hexcode for v in values))
