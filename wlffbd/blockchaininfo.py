# -*- coding: utf-8 -*-
'''blockchain.info related functions'''
import json
import os
import urllib
import urllib2
import time

BLOCKCHAIN_URI = 'https://blockchain.info'


def make_blockchain_url(path, uri=BLOCKCHAIN_URI, **kwargs):
    '''Return a blockchain.info URL with the given path appended to the uri and urlencoded keyword arguments appended.'''
    return '{}/{}?{}'.format(uri, path, urllib.urlencode(kwargs))


def get_blockchain_request(path, uri=BLOCKCHAIN_URI, **kwargs):
    '''Return a response from urllib2.urlopen with the URL built by concatenating the uri, path, and urlencoded keyword arguments.'''
    return urllib2.urlopen(make_blockchain_url(path, uri=uri, **kwargs))


def get_blockchain_rawaddr(address, limit=50, offset=0, silent=True, uri=BLOCKCHAIN_URI):
    error = True
    while error:
        try:
            dat = get_blockchain_request('rawaddr/{}'.format(address), format=json, limit=limit, offset=offset, uri=uri)
            error = False
        except urllib2.URLError, e:
            if not silent:
                print('Error: Trying to open address {} from blockchain.info: '.format(address, e.reason))
    return json.loads(dat.read().decode())


def get_txs_from_blockchain_json(data):
    return [tx.get('hash').encode('ascii') for tx in data.get('txs', [])]


def get_tx_from_online(address, limit=50, sleep=1, callback=None):
    address = address.rstrip('\r\n')
    offset = 0
    data = get_blockchain_rawaddr(address, limit=limit, offset=offset, silent=False)
    n_tx = data['n_tx']
    txlist = get_txs_from_blockchain_json(data)

    while len(txlist) < n_tx:
        if callback and callable(callback):
            callback(txlist, n_tx)
        offset += 50
        txlist.extend(get_txs_from_blockchain_json(get_blockchain_rawaddr(address, limit=limit, offset=offset, silent=True)))
        # Lets be nice to blockchain.info
        if sleep:
            time.sleep(sleep)

    return txlist
