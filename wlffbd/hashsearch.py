# -*- coding: utf-8 -*-
'''Wikileaks hash search functions'''
import json
from .filesystem import read
from binascii import hexlify

hashes = {hash: json.loads(read('data/wlhashes/{}.json'.format(hash)))
          for hash in ('md5', 'sha1', 'sha256')}

def check_hash(hexcode, sumcheck):
    '''
    This will return whether or not a wikileaks file hash is inside the blockchain
    '''
    return ' '.join('{}'.format(key)
                    for key, values in hashes[sumcheck].iteritems()
                    if all(hexlify(v.encode('utf8')) in hexcode for v in values))
